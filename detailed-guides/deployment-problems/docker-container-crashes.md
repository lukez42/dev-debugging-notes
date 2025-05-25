# Debugging Docker Container Crashes

## Problem Overview
Docker containers can crash for various reasons, from application errors to resource constraints. This guide provides a comprehensive approach to diagnosing, fixing, and preventing container crashes in production environments.

## Prerequisites
- Docker installed and running
- Access to container logs
- Basic understanding of Linux commands
- Monitoring tools (optional but recommended)

## Step-by-Step Solution

### 1. Initial Investigation
- Check container status:
  ```bash
  # List all containers (including stopped)
  docker ps -a
  
  # Check container logs
  docker logs <container_id>
  
  # Check container resource usage
  docker stats <container_id>
  
  # Inspect container details
  docker inspect <container_id>
  ```

### 2. Root Cause Analysis
Common causes of container crashes:
1. **Application Errors**: Unhandled exceptions, segmentation faults
2. **Resource Limits**: Memory/CPU constraints, disk space
3. **Network Issues**: Connection timeouts, DNS problems
4. **Configuration Problems**: Incorrect environment variables, missing volumes
5. **System Issues**: Host system problems, Docker daemon issues

### 3. Solution Implementation
```bash
# 1. Enable container restart policy
docker run --restart unless-stopped myapp:latest

# 2. Set resource limits
docker run \
  --memory="2g" \
  --memory-swap="2g" \
  --cpus="1.5" \
  myapp:latest

# 3. Configure health checks
docker run \
  --health-cmd="curl -f http://localhost:8080/health || exit 1" \
  --health-interval=30s \
  --health-timeout=10s \
  --health-retries=3 \
  myapp:latest

# 4. Example Dockerfile with best practices
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Create non-root user
RUN useradd -m myuser
USER myuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT}/health || exit 1

# Run application
CMD ["python", "app.py"]
```

### 4. Verification
- Monitor container health:
  ```bash
  # Check container status
  docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Health}}"
  
  # Monitor logs in real-time
  docker logs -f <container_id>
  
  # Check resource usage
  docker stats <container_id>
  
  # Test container connectivity
  docker exec <container_id> curl -I http://localhost:8080/health
  ```

## Alternative Solutions
1. **Docker Compose**
   - Pros: Easier management, service dependencies
   - Cons: Additional complexity
   - When to use: Multi-container applications

2. **Kubernetes**
   - Pros: Advanced orchestration, auto-scaling
   - Cons: Complex setup, overkill for simple apps
   - When to use: Production, large-scale deployments

3. **Systemd Service**
   - Pros: Native system integration
   - Cons: Less portable
   - When to use: Single-host deployments

## Prevention and Best Practices
1. **Container Design**
   - Use official base images
   - Implement proper health checks
   - Set resource limits
   - Use non-root users
   - Handle signals properly

2. **Monitoring**
   - Set up logging aggregation
   - Monitor resource usage
   - Implement alerting
   - Use container orchestration

3. **Security**
   - Regular image updates
   - Security scanning
   - Minimal base images
   - Proper secrets management

## Troubleshooting
1. **Container Exits Immediately**
   - Symptoms: Container starts and stops
   - Solution:
     ```bash
     # Check exit code
     docker inspect <container_id> --format='{{.State.ExitCode}}'
     
     # Run with interactive shell
     docker run -it --entrypoint /bin/bash myapp:latest
     
     # Check application logs
     docker logs <container_id>
     ```

2. **Memory Issues**
   - Symptoms: OOM (Out of Memory) kills
   - Solution:
     ```bash
     # Increase memory limit
     docker run --memory="4g" myapp:latest
     
     # Check memory usage
     docker stats <container_id>
     
     # Analyze memory usage
     docker exec <container_id> free -m
     ```

3. **Network Problems**
   - Symptoms: Connection timeouts, DNS issues
   - Solution:
     ```bash
     # Check network configuration
     docker network inspect bridge
     
     # Test network connectivity
     docker exec <container_id> ping -c 4 google.com
     
     # Check DNS resolution
     docker exec <container_id> nslookup google.com
     ```

## References
- [Docker Documentation](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Container Health Checks](https://docs.docker.com/engine/reference/builder/#healthcheck)

## Tags
#detailed-guide #docker #deployment #troubleshooting #complexity-high 