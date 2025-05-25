# Debugging Node.js Memory Leaks

## Problem Overview
Memory leaks in Node.js applications can lead to degraded performance, increased response times, and eventual application crashes. This guide provides a comprehensive approach to identifying, fixing, and preventing memory leaks in Node.js applications.

## Prerequisites
- Node.js application (version 12 or higher recommended)
- Access to application logs
- Basic understanding of JavaScript and Node.js
- Monitoring tools (optional but recommended)

## Step-by-Step Solution

### 1. Initial Investigation
- Check memory usage:
  ```bash
  # Get process memory usage
  node --inspect app.js
  
  # Monitor memory in real-time
  node --inspect --expose-gc app.js
  
  # Check heap snapshots
  curl -X POST http://localhost:9229/json/protocol/Runtime.takeHeapSnapshot
  ```

- Use Chrome DevTools:
  1. Open Chrome and navigate to `chrome://inspect`
  2. Click on "Open dedicated DevTools for Node"
  3. Connect to your Node.js application
  4. Use Memory tab to take heap snapshots

### 2. Root Cause Analysis
Common causes of memory leaks:
1. **Closure Issues**: Unclosed event listeners, callbacks
2. **Global Variables**: Accumulating data in global scope
3. **Caching**: Unbounded caches, missing cache invalidation
4. **Stream Handling**: Unclosed streams, missing error handling
5. **Timer Issues**: Uncleared intervals/timeouts

### 3. Solution Implementation
```javascript
// 1. Proper event listener cleanup
class EventEmitter {
  constructor() {
    this.listeners = new Map();
  }

  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event).add(callback);
    return () => this.off(event, callback); // Return cleanup function
  }

  off(event, callback) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).delete(callback);
    }
  }

  cleanup() {
    this.listeners.clear();
  }
}

// 2. Bounded cache implementation
class BoundedCache {
  constructor(maxSize = 1000) {
    this.cache = new Map();
    this.maxSize = maxSize;
  }

  set(key, value) {
    if (this.cache.size >= this.maxSize) {
      // Remove oldest entry
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(key, value);
  }

  get(key) {
    return this.cache.get(key);
  }

  clear() {
    this.cache.clear();
  }
}

// 3. Proper stream handling
const fs = require('fs');

function processFile(filename) {
  return new Promise((resolve, reject) => {
    const stream = fs.createReadStream(filename);
    let data = '';

    stream.on('data', chunk => {
      data += chunk;
    });

    stream.on('end', () => {
      resolve(data);
    });

    stream.on('error', error => {
      reject(error);
    });
  });
}

// 4. Timer management
class TimerManager {
  constructor() {
    this.timers = new Set();
  }

  setTimeout(callback, delay) {
    const timer = setTimeout(() => {
      this.timers.delete(timer);
      callback();
    }, delay);
    this.timers.add(timer);
    return timer;
  }

  clearAll() {
    this.timers.forEach(timer => clearTimeout(timer));
    this.timers.clear();
  }
}
```

### 4. Verification
- Monitor memory usage:
  ```javascript
  // Add memory monitoring
  setInterval(() => {
    const used = process.memoryUsage();
    console.log(`Memory usage: ${Math.round(used.heapUsed / 1024 / 1024)}MB`);
  }, 1000);

  // Force garbage collection (development only)
  if (global.gc) {
    global.gc();
  }
  ```

## Alternative Solutions
1. **Memory Profiling Tools**
   - Pros: Detailed analysis, visualization
   - Cons: Overhead, complex setup
   - When to use: Deep debugging, production issues

2. **APM Tools**
   - Pros: Real-time monitoring, alerts
   - Cons: Cost, additional infrastructure
   - When to use: Production environments

3. **Manual Memory Management**
   - Pros: Full control, no overhead
   - Cons: Error-prone, time-consuming
   - When to use: Critical performance sections

## Prevention and Best Practices
1. **Code Structure**
   - Use proper scoping
   - Implement cleanup methods
   - Avoid global variables
   - Use weak references when appropriate

2. **Monitoring**
   - Set up memory monitoring
   - Implement leak detection
   - Use APM tools
   - Regular profiling

3. **Development Practices**
   - Code reviews
   - Memory testing
   - Regular profiling
   - Documentation

## Troubleshooting
1. **High Memory Usage**
   - Symptoms: Growing heap, slow performance
   - Solution:
     ```javascript
     // Add memory monitoring
     const heapUsed = process.memoryUsage().heapUsed;
     console.log(`Heap used: ${Math.round(heapUsed / 1024 / 1024)}MB`);
     
     // Take heap snapshot
     const heapdump = require('heapdump');
     heapdump.writeSnapshot(`./heap-${Date.now()}.heapsnapshot`);
     ```

2. **Event Listener Leaks**
   - Symptoms: Growing number of listeners
   - Solution:
     ```javascript
     // Check listener count
     const listenerCount = emitter.listenerCount('event');
     console.log(`Active listeners: ${listenerCount}`);
     
     // Remove all listeners
     emitter.removeAllListeners('event');
     ```

3. **Timer Leaks**
   - Symptoms: Multiple timers, high CPU usage
   - Solution:
     ```javascript
     // List active timers
     const activeTimers = process._getActiveHandles()
       .filter(h => h.constructor.name === 'Timer');
     console.log(`Active timers: ${activeTimers.length}`);
     
     // Clear all timers
     activeTimers.forEach(timer => clearTimeout(timer));
     ```

## References
- [Node.js Memory Management](https://nodejs.org/en/docs/guides/memory-management/)
- [Chrome DevTools Memory Profiling](https://developer.chrome.com/docs/devtools/memory-problems/)
- [Node.js Performance Best Practices](https://nodejs.org/en/docs/guides/simple-profiling/)

## Tags
#detailed-guide #nodejs #performance #memory #complexity-high 