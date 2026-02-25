import json
import random
import os

def generate_coding_dataset(output_dir="src/data", target_train=1000, target_val=300):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Technical Facts (The 'Curated' Data)
    qa_data = [
        ("Python", "Method Resolution Order (MRO)", "defines how Python searches for methods in a multi-inheritance hierarchy using the C3 Linearization algorithm. This ensures that parent classes are checked only once and in a consistent, left-to-right order."),
        ("JS", "Microtask Queue", "prioritizes Promise callbacks and process.nextTick over the standard Task Queue. This architecture ensures high-priority asynchronous logic executes immediately after the current task finishes."),
        ("Rust", "The Borrow Checker", "enforces strict compile-time rules: either one mutable reference or multiple immutable references to a resource. This system eliminates data races and manual memory leaks without a garbage collector."),
        ("Go", "Goroutine Scheduling", "uses an M:N model with work-stealing to multiplex thousands of lightweight goroutines onto a few OS threads. This approach minimizes context-switching overhead and maximizes CPU efficiency."),
        ("SQL", "B-Tree Indexing", "organizes data in a balanced tree structure to support O(log n) lookups and efficient range queries. It is the gold standard for relational databases where filtered sorting is a common operation."),
        ("Docker", "UnionFS (Layering)", "allows images to share read-only disk layers. Each container only creates a thin writable layer on top, which drastically reduces storage fingerprints and speeds up deployment cycles."),
        ("Java", "The G1 Garbage Collector", "manages the heap in flexible regions to prioritize cleaning segments with the most garbage (Garbage First). It helps maintain predictable pause times in high-memory enterprise applications."),
        ("C++", "RAII (Resource Acquisition Is Initialization)", "binds the resource lifecycle to the scope of an object. Constructors acquire resources, and destructors release them, ensuring zero memory leaks even in the event of hardware exceptions.")
    ]

    # CLEANED: No prepositions here. We control the 'for'/'in'/'at' in the template.
    scenarios = [
        "a high-throughput fintech API",
        "a distributed microservices architecture", 
        "a legacy monolith undergoing cloud migration",
        "a real-time analytics engine",
        "a multi-tenant SaaS application",
        "a resource-constrained IoT device",
        "a global content delivery network",
        "a secure banking perimeter"
    ]

    # VARIETY: Distinct intro hooks to prevent response bias
    hooks = [
        "From an engineering perspective,",
        "Within the context of a modern production environment,",
        "When evaluating system architecture,",
        "A critical factor to consider is how",
        "In professional software development,",
        "Technically speaking,",
        "Regarding optimal performance,",
        "The primary advantage of this approach is that"
    ]

    # VARIETY: Distinct conclusions
    conclusions = [
        "This architectural choice is non-negotiable for enterprise stability.",
        "It effectively prevents system bottlenecks during high-load periods.",
        "This ensures the application remains resilient and horizontally scalable.",
        "Implementing this correctly is vital for long-term project maintainability.",
        "It provides a robust foundation for modern cloud-native deployments.",
        "This is the most effective way to guarantee deterministic behavior."
    ]

    extraction_samples = [
        {"topic": "Python", "code": "class API:\n    @auth_required\n    @rate_limit(count=100, period='1m')\n    def fetch(self): pass", "instr": "Identify the rate limiting parameters (count and period).", "out": "count: 100, period: 1m"},
        {"topic": "SQL", "code": "SELECT u.name, o.cost FROM users u JOIN orders o ON u.id = o.user_id WHERE o.status = 'DELIVERED';", "instr": "Extract the join condition and the filtering status value.", "out": "join: u.id = o.user_id, status: 'DELIVERED'"},
        {"topic": "Kubernetes", "code": "spec:\n  containers:\n  - name: proxy\n    image: envoyproxy/envoy:v1.22.0\n    ports:\n    - containerPort: 8080", "instr": "Extract the proxy image name and its specific version tag.", "out": "image: envoyproxy/envoy, version: v1.22.0"},
        {"topic": "React", "code": "const [data, setData] = useState(null);\nuseEffect(() => { load(id); }, [id, config]);", "instr": "Identify all variables in the dependency array for the Hook.", "out": "id, config"}
    ]

    def create_sample(stype):
        topic, concept, detail = random.choice(qa_data)
        scen = random.choice(scenarios)
        hook = random.choice(hooks)
        conc = random.choice(conclusions)
        noise = random.randint(100, 999)
        
        if stype == "QA":
            return {
                "instruction": f"Explain the core engineering principles of {concept} in {topic} for {scen}. (REF-{noise})",
                "input": "",
                "output": f"{hook} {concept} in {topic} {detail} This logic is critical for {scen}, as {conc}",
                "type": "QA"
            }
        elif stype == "Reasoning":
            return {
                "instruction": f"Analyze the technical trade-offs of using {concept} in {topic} when building {scen}. (CASE-{noise})",
                "input": "",
                "output": f"When configuring {scen}, {hook} {topic}'s {concept} {detail} By prioritizing these trade-offs, developers ensure {conc}",
                "type": "Reasoning"
            }
        else: # Extraction
            base = random.choice(extraction_samples)
            return {
                "instruction": f"[{base['topic']}] Technical Extraction: {base['instr']} (ID-{noise})",
                "input": f"// Application Domain: {scen}\n{base['code']}",
                "output": base['out'],
                "type": "Extraction"
            }

    samples = []
    seen = set()
    
    def get_unique_sample(stype):
        new_sample = create_sample(stype)
        identity = new_sample['instruction'] + new_sample['input']
        attempts = 0
        while identity in seen and attempts < 100:
            new_sample = create_sample(stype)
            identity = new_sample['instruction'] + new_sample['input']
            attempts += 1
        seen.add(identity)
        return new_sample

    total_target = target_train + target_val
    per_type = total_target // 3
    
    raw_list = ["QA"] * per_type + ["Reasoning"] * per_type + ["Extraction"] * (total_target - 2 * per_type)
    random.shuffle(raw_list)

    all_samples = [get_unique_sample(t) for t in raw_list]
    
    train_data = all_samples[:target_train]
    val_data = all_samples[target_train:]
    
    with open(os.path.join(output_dir, "train.jsonl"), "w") as f:
        for s in train_data: f.write(json.dumps(s) + "\n")
    with open(os.path.join(output_dir, "val.jsonl"), "w") as f:
        for s in val_data: f.write(json.dumps(s) + "\n")
            
    print(f"SUCCESS: Generated {len(train_data)} train and {len(val_data)} val samples (Organic Style).")

if __name__ == "__main__":
    generate_coding_dataset()