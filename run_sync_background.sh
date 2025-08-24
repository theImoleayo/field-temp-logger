#!/bin/bash
# Run ThingSpeak sync service in a screen session for easy management

SCRIPT_DIR="/home/theimoleayo/Git_Clone/Field_Worker_Monitoring"
SESSION_NAME="thingspeak-sync"

case "$1" in
    start)
        echo "Starting ThingSpeak sync service in background..."
        
        # Check if session already exists
        if screen -list | grep -q "${SESSION_NAME}"; then
            echo "Sync service is already running!"
            echo "Use './run_sync_background.sh status' to check status"
            echo "Use './run_sync_background.sh stop' to stop it"
            exit 1
        fi
        
        # Start the sync service in a detached screen session
        cd "${SCRIPT_DIR}"
        screen -dmS "${SESSION_NAME}" python3 thingspeak_sync.py
        
        # Give it a moment to start
        sleep 2
        
        # Check if it's running
        if screen -list | grep -q "${SESSION_NAME}"; then
            echo "✓ Sync service started successfully in background"
            echo "Use './run_sync_background.sh logs' to see logs"
            echo "Use './run_sync_background.sh stop' to stop it"
        else
            echo "✗ Failed to start sync service"
        fi
        ;;
        
    stop)
        echo "Stopping ThingSpeak sync service..."
        
        if screen -list | grep -q "${SESSION_NAME}"; then
            screen -S "${SESSION_NAME}" -X quit
            echo "✓ Sync service stopped"
        else
            echo "Sync service is not running"
        fi
        ;;
        
    status)
        echo "ThingSpeak sync service status:"
        
        if screen -list | grep -q "${SESSION_NAME}"; then
            echo "✓ Service is running"
            echo ""
            echo "Screen sessions:"
            screen -list | grep "${SESSION_NAME}"
        else
            echo "✗ Service is not running"
        fi
        ;;
        
    logs)
        echo "Connecting to sync service logs..."
        echo "Press Ctrl+A then D to detach (leave service running)"
        echo "Press Ctrl+C to stop the service"
        echo ""
        echo "Starting in 3 seconds..."
        sleep 3
        
        if screen -list | grep -q "${SESSION_NAME}"; then
            screen -r "${SESSION_NAME}"
        else
            echo "✗ Sync service is not running"
        fi
        ;;
        
    restart)
        echo "Restarting ThingSpeak sync service..."
        $0 stop
        sleep 2
        $0 start
        ;;
        
    test)
        echo "Running one-time sync test..."
        cd "${SCRIPT_DIR}"
        python3 thingspeak_sync.py --once
        ;;
        
    *)
        echo "Usage: $0 {start|stop|status|logs|restart|test}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the sync service in background"
        echo "  stop    - Stop the sync service"
        echo "  status  - Check if service is running"
        echo "  logs    - Connect to service logs (Ctrl+A then D to detach)"
        echo "  restart - Restart the service"
        echo "  test    - Run a one-time sync test"
        echo ""
        echo "Note: This uses 'screen' to run the service in background."
        echo "Make sure 'screen' is installed: sudo apt install screen"
        exit 1
        ;;
esac

exit 0
