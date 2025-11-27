#!/bin/bash

# Multi-Agent Orchestrator - Quick Start Script
# This script helps you quickly start and manage the multi-agent orchestrator service

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    print_success "Docker is installed"
}

# Check if Docker Compose is installed
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    print_success "Docker Compose is installed"
}

# Build the service
build_service() {
    print_header "Building Multi-Agent Orchestrator Service"
    docker-compose build multi_agent_orchestrator
    print_success "Service built successfully"
}

# Start the service
start_service() {
    print_header "Starting Multi-Agent Orchestrator Service"
    docker-compose up -d ollama multi_agent_orchestrator
    print_success "Service started successfully"
    
    print_info "Waiting for services to be healthy..."
    sleep 10
    
    # Check health
    if docker inspect --format='{{.State.Health.Status}}' multi_agent_orchestrator 2>/dev/null | grep -q "healthy"; then
        print_success "Service is healthy"
    else
        print_warning "Service is starting... (may take up to 40 seconds)"
    fi
}

# Stop the service
stop_service() {
    print_header "Stopping Multi-Agent Orchestrator Service"
    docker-compose stop multi_agent_orchestrator
    print_success "Service stopped successfully"
}

# View logs
view_logs() {
    print_header "Viewing Service Logs (Ctrl+C to exit)"
    docker-compose logs -f multi_agent_orchestrator
}

# Check status
check_status() {
    print_header "Service Status"
    
    # Check if container is running
    if docker ps | grep -q multi_agent_orchestrator; then
        print_success "Container is running"
        
        # Check health
        health=$(docker inspect --format='{{.State.Health.Status}}' multi_agent_orchestrator 2>/dev/null || echo "unknown")
        if [ "$health" = "healthy" ]; then
            print_success "Health status: healthy"
        else
            print_warning "Health status: $health"
        fi
        
        # Show resource usage
        echo ""
        print_info "Resource Usage:"
        docker stats --no-stream multi_agent_orchestrator
    else
        print_error "Container is not running"
    fi
}

# Enter container
enter_container() {
    print_header "Entering Container Shell"
    docker exec -it multi_agent_orchestrator bash
}

# Run interactive mode
run_interactive() {
    print_header "Running Interactive Mode"
    docker exec -it multi_agent_orchestrator python agents/interactive.py
}

# Run demo
run_demo() {
    print_header "Running Demo"
    docker exec -it multi_agent_orchestrator python agents/demo.py
}

# Run examples
run_examples() {
    print_header "Running Examples"
    docker exec -it multi_agent_orchestrator python agents/main.py
}

# Backup data
backup_data() {
    print_header "Backing Up Agent Memories and Logs"
    
    timestamp=$(date +%Y%m%d_%H%M%S)
    backup_dir="backups/$timestamp"
    mkdir -p "$backup_dir"
    
    # Backup memories
    print_info "Backing up agent memories..."
    docker run --rm -v orchestrator_data:/data -v "$(pwd)/$backup_dir":/backup \
        alpine tar czf /backup/agent_memories.tar.gz -C /data .
    print_success "Agent memories backed up to $backup_dir/agent_memories.tar.gz"
    
    # Backup logs
    print_info "Backing up logs..."
    docker run --rm -v orchestrator_logs:/data -v "$(pwd)/$backup_dir":/backup \
        alpine tar czf /backup/logs.tar.gz -C /data .
    print_success "Logs backed up to $backup_dir/logs.tar.gz"
    
    print_success "Backup completed: $backup_dir"
}

# Restore data
restore_data() {
    if [ -z "$1" ]; then
        print_error "Please specify backup directory: ./orchestrator.sh restore backups/TIMESTAMP"
        exit 1
    fi
    
    backup_dir="$1"
    
    if [ ! -d "$backup_dir" ]; then
        print_error "Backup directory not found: $backup_dir"
        exit 1
    fi
    
    print_header "Restoring Data from $backup_dir"
    
    # Restore memories
    if [ -f "$backup_dir/agent_memories.tar.gz" ]; then
        print_info "Restoring agent memories..."
        docker run --rm -v orchestrator_data:/data -v "$(pwd)/$backup_dir":/backup \
            alpine sh -c "cd /data && tar xzf /backup/agent_memories.tar.gz"
        print_success "Agent memories restored"
    fi
    
    # Restore logs
    if [ -f "$backup_dir/logs.tar.gz" ]; then
        print_info "Restoring logs..."
        docker run --rm -v orchestrator_logs:/data -v "$(pwd)/$backup_dir":/backup \
            alpine sh -c "cd /data && tar xzf /backup/logs.tar.gz"
        print_success "Logs restored"
    fi
    
    print_success "Restore completed"
}

# Clean up
cleanup() {
    print_header "Cleaning Up"
    
    print_warning "This will remove the container and volumes. Are you sure? (y/N)"
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        docker-compose down multi_agent_orchestrator
        docker volume rm orchestrator_data orchestrator_logs 2>/dev/null || true
        print_success "Cleanup completed"
    else
        print_info "Cleanup cancelled"
    fi
}

# Show help
show_help() {
    cat << EOF
Multi-Agent Orchestrator - Quick Start Script

Usage: ./orchestrator.sh [command]

Commands:
    build           Build the service
    start           Start the service
    stop            Stop the service
    restart         Restart the service
    status          Check service status
    logs            View service logs
    shell           Enter container shell
    interactive     Run interactive mode
    demo            Run demo
    examples        Run examples
    backup          Backup agent memories and logs
    restore [dir]   Restore from backup directory
    cleanup         Remove container and volumes
    help            Show this help message

Examples:
    ./orchestrator.sh build
    ./orchestrator.sh start
    ./orchestrator.sh logs
    ./orchestrator.sh interactive
    ./orchestrator.sh backup
    ./orchestrator.sh restore backups/20240115_120000

For more information, see services/multi_agent_orchestrator/README.md
EOF
}

# Main script
main() {
    case "${1:-help}" in
        build)
            check_docker
            check_docker_compose
            build_service
            ;;
        start)
            check_docker
            check_docker_compose
            start_service
            ;;
        stop)
            check_docker
            check_docker_compose
            stop_service
            ;;
        restart)
            check_docker
            check_docker_compose
            stop_service
            sleep 2
            start_service
            ;;
        status)
            check_docker
            check_status
            ;;
        logs)
            check_docker
            view_logs
            ;;
        shell)
            check_docker
            enter_container
            ;;
        interactive)
            check_docker
            run_interactive
            ;;
        demo)
            check_docker
            run_demo
            ;;
        examples)
            check_docker
            run_examples
            ;;
        backup)
            check_docker
            backup_data
            ;;
        restore)
            check_docker
            restore_data "$2"
            ;;
        cleanup)
            check_docker
            check_docker_compose
            cleanup
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
