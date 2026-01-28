const Logger = require('../utils/logger');

module.exports = ({ app }) => {
    const routes = require('../routes');

    // Recursive function to count all routes in a router
    const countRoutes = (router) => {
        if (!router || !router.stack) return 0;

        let count = 0;
        router.stack.forEach((layer) => {
            if (layer.route) {
                // This is an actual route endpoint
                count++;
            } else if (layer.name === 'router' && layer.handle) {
                // This is a nested router, recurse into it
                count += countRoutes(layer.handle);
            }
        });

        return count;
    };

    // Count routes before mounting
    const totalRoutes = countRoutes(routes);

    // Mount routes
    app.use('/api', routes);

    return totalRoutes;
};
