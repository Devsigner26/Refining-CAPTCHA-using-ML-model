        let mouseMovements = [];
        let clickTimes = [];
        let scrollDepth = 0;
        let pageLoadTime = Date.now();

        // Capture mouse movements
        document.addEventListener("mousemove", (e) => {
            mouseMovements.push({x: e.clientX, y: e.clientY, time: Date.now()});
        });

        // Capture click speed (time between clicks)
        document.addEventListener("click", (e) => {
            let clickTime = Date.now();
            if (clickTimes.length > 0) {
                let lastClickTime = clickTimes[clickTimes.length - 1];
                clickTimes.push(clickTime - lastClickTime);
            } else {
                clickTimes.push(0); // First click has no previous click time
            }
        });

        // Capture scroll depth
        window.addEventListener("scroll", () => {
            let currentScrollDepth = window.scrollY + window.innerHeight;
            if (currentScrollDepth > scrollDepth) {
                scrollDepth = currentScrollDepth;
            }
        });

        // Capture device orientation
        let deviceOrientation = window.orientation || 0;

        // Send data to backend every 10 seconds
        setInterval(() => {
            let timeOnPage = (Date.now() - pageLoadTime) / 1000;
            let data = {
                mouse_movement: mouseMovements,
                click_speed: clickTimes,
                device_orientation: deviceOrientation,
                scroll_depth: scrollDepth,
                time_on_page: timeOnPage,
                label: "human" // Label can be set for supervised learning (use bot for testing bot data)
            };
            // Send data to backend
            fetch("http://localhost:8000/collect_data", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            }).then(response => response.json()).then(data => console.log(data));

            // Reset data for the next interval
            mouseMovements = [];
            clickTimes = [];
        }, 10000); // Send data every 10 seconds
