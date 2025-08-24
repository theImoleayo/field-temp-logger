#!/bin/bash
# Service management script for ThingSpeak sync service

SERVICE_NAME="thingspeak-sync"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
CURRENT_DIR="/home/theimoleayo/Git_Clone/Field_Worker_Monitoring"

case "$1" in
    install)
        echo "Installing ThingSpeak sync service..."
        
        # Copy service file to systemd directory
        sudo cp "${CURRENT_DIR}/${SERVICE_NAME}.service" "${SERVICE_FILE}"
        
        # Reload systemd to recognize the new service
        sudo systemctl daemon-reload
        
        # Enable the service to start on boot
        sudo systemctl enable ${SERVICE_NAME}
        
        echo "✓ Service installed and enabled"
        echo "Use './manage_sync_service.sh start' to start the service"
        ;;
        
    start)
        echo "Starting ThingSpeak sync service..."
        sudo systemctl start ${SERVICE_NAME}
        
        # Check if it started successfully
        if sudo systemctl is-active --quiet ${SERVICE_NAME}; then
            echo "✓ Service started successfully"
        else
            echo "✗ Failed to start service"
            echo "Check logs with: sudo journalctl -u ${SERVICE_NAME} -f"
        fi
        ;;
        
    stop)
        echo "Stopping ThingSpeak sync service..."
        sudo systemctl stop ${SERVICE_NAME}
        echo "✓ Service stopped"
        ;;
        
    restart)
        echo "Restarting ThingSpeak sync service..."
        sudo systemctl restart ${SERVICE_NAME}
        echo "✓ Service restarted"
        ;;
        
    status)
        echo "ThingSpeak sync service status:"
        sudo systemctl status ${SERVICE_NAME}
        ;;
        
    logs)
        echo "ThingSpeak sync service logs (press Ctrl+C to exit):"
        sudo journalctl -u ${SERVICE_NAME} -f
        ;;
        
    uninstall)
        echo "Uninstalling ThingSpeak sync service..."
        
        # Stop and disable the service
        sudo systemctl stop ${SERVICE_NAME} 2>/dev/null
        sudo systemctl disable ${SERVICE_NAME} 2>/dev/null
        
        # Remove service file
        sudo rm -f "${SERVICE_FILE}"
        
        # Reload systemd
        sudo systemctl daemon-reload
        
        echo "✓ Service uninstalled"
        ;;
        
    test)
        echo "Running one-time sync test..."
        cd "${CURRENT_DIR}"
        python3 thingspeak_sync.py --once
        ;;
        
    *)
        echo "Usage: $0 {install|start|stop|restart|status|logs|uninstall|test}"
        echo ""
        echo "Commands:"
        echo "  install   - Install the systemd service"
        echo "  start     - Start the service"
        echo "  stop      - Stop the service"
        echo "  restart   - Restart the service"
        echo "  status    - Show service status"
        echo "  logs      - Show service logs (real-time)"
        echo "  uninstall - Remove the service"
        echo "  test      - Run a one-time sync test"
        exit 1
        ;;
esac

exit 0
