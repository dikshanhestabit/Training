# Linux Internals Exploration (Inside Docker)

This document records the findings from exploring the Linux environment inside the Node.js container.

## Commands Executed

### 1. Basic Navigation and File System
Command: `ls -la`
Output:
```text
total 28
drwxr-xr-x    1 root     root          4096 Feb  3 11:15 .
drwxr-xr-x    1 root     root          4096 Feb  3 11:08 ..
-rw-rw-r--    1 root     root           573 Feb  3 10:59 Dockerfile
-rw-rw-r--    1 root     root           334 Feb  3 10:59 index.js
-rw-rw-r--    1 root     root          2189 Feb  3 11:09 linux-in-container.md
-rw-r--r--    1 root     root           217 Feb  3 11:08 package-lock.json
-rw-rw-r--    1 root     root           212 Feb  3 10:59 package.json
```

### 2. Process Management
Command: `ps aux`
Output:
```text
PID   USER     TIME  COMMAND
    1 root      0:00 npm start
   18 root      0:00 node index.js
   25 root      0:00 /bin/sh
   32 root      0:00 ps aux
```

### 3. Disk Usage
Command: `df -h`
Output:
```text
Filesystem                Size      Used Available Use% Mounted on
overlay                 467.3G     30.8G    412.8G   7% /
tmpfs                    64.0M         0     64.0M   0% /dev
shm                      64.0M         0     64.0M   0% /dev/shm
/dev/nvme0n1p2          467.3G     30.8G    412.8G   7% /etc/resolv.conf
/dev/nvme0n1p2          467.3G     30.8G    412.8G   7% /etc/hostname
/dev/nvme0n1p2          467.3G     30.8G    412.8G   7% /etc/hosts
tmpfs                    15.4G         0     15.4G   0% /proc/asound
tmpfs                    15.4G         0     15.4G   0% /proc/acpi
tmpfs                    64.0M         0     64.0M   0% /proc/interrupts
tmpfs                    64.0M         0     64.0M   0% /proc/kcore
tmpfs                    64.0M         0     64.0M   0% /proc/keys
tmpfs                    64.0M         0     64.0M   0% /proc/latency_stats
tmpfs                    64.0M         0     64.0M   0% /proc/timer_list
tmpfs                    15.4G         0     15.4G   0% /proc/scsi
tmpfs                    15.4G         0     15.4G   0% /sys/firmware
tmpfs                    15.4G         0     15.4G   0% /sys/devices/virtual/powercap
tmpfs                    15.4G         0     15.4G   0% /sys/devices/system/cpu/cpu0/thermal_throttle
tmpfs                    15.4G         0     15.4G   0% /sys/devices/system/cpu/cpu1/thermal_throttle
tmpfs                    15.4G         0     15.4G   0% /sys/devices/system/cpu/cpu2/thermal_throttle
tmpfs                    15.4G         0     15.4G   0% /sys/devices/system/cpu/cpu3/thermal_throttle
tmpfs                    15.4G         0     15.4G   0% /sys/devices/system/cpu/cpu4/thermal_throttle
tmpfs                    15.4G         0     15.4G   0% /sys/devices/system/cpu/cpu5/thermal_throttle
tmpfs                    15.4G         0     15.4G   0% /sys/devices/system/cpu/cpu6/thermal_throttle
tmpfs                    15.4G         0     15.4G   0% /sys/devices/system/cpu/cpu7/thermal_throttle
tmpfs                    15.4G         0     15.4G   0% /sys/devices/system/cpu/cpu8/thermal_throttle
tmpfs                    15.4G         0     15.4G   0% /sys/devices/system/cpu/cpu9/thermal_throttle
tmpfs                    15.4G         0     15.4G   0% /sys/devices/system/cpu/cpu10/thermal_throttle
tmpfs                    15.4G         0     15.4G   0% /sys/devices/system/cpu/cpu11/thermal_throttle
```

### 4. Logging
Command: `ls -l /var/log`
Output:
```text
total 8
-rw-r--r--    1 root     root          5672 Jan 28 03:31 apk.log
```

### 5. OS Information
Command: `cat /etc/os-release`
Output:
```text
NAME="Alpine Linux"
ID=alpine
VERSION_ID=3.23.3
PRETTY_NAME="Alpine Linux v3.23"
HOME_URL="https://alpinelinux.org/"
BUG_REPORT_URL="https://gitlab.alpinelinux.org/alpine/aports/-/issues"
```

### 6. Resource Monitoring
Command: `top -n 1`
Output:
```text
Mem: 14789056K used, 17496424K free, 1256240K shrd, 240692K buff, 6147800K cach
CPU:   1% usr   0% sys   0% nic  97% idle   0% io   0% irq   0% sirq
Load average: 1.89 0.95 0.66 1/2623 59
  PID  PPID USER     STAT   VSZ %VSZ CPU %CPU COMMAND
    1     0 root     S     682m   2%   4   0% npm start
   18     1 root     S     646m   2%   0   0% node index.js
   54     0 root     R     1636   0%   2   0% top -n 1
```
