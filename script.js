$(document).ready(function() {
    // Initialize select2 for item selection
    $('#item-select').select2({
        placeholder: "Select items to pick...",
        allowClear: true
    });
    
    // Load items from the API
    $.get('/api/items', function(data) {
        data.forEach(function(item) {
            var option = new Option(
                `${item.item_id} - ${item.item_name} (${item.current_location})`, 
                item.item_id
            );
            $('#item-select').append(option);
        });
    });
    
    // Handle optimize button click
    $('#optimize-btn').click(function() {
        var selectedItems = $('#item-select').val();
        if (!selectedItems || selectedItems.length === 0) {
            alert('Please select at least one item');
            return;
        }
        
        $.ajax({
            url: '/api/optimize',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ items: selectedItems }),
            success: function(response) {
                displayOptimizedRoute(response);
                drawRouteVisualization(response.optimized_route);
            },
            error: function() {
                alert('Error optimizing route');
            }
        });
    });
    
    function displayOptimizedRoute(routeData) {
        var routeSteps = $('#route-steps');
        routeSteps.empty();
        
        if (routeData.optimized_route.length === 0) {
            routeSteps.append('<div class="route-step">No items selected or locations not found</div>');
            return;
        }
        
        routeData.optimized_route.forEach(function(step, index) {
            routeSteps.append(`
                <div class="route-step">
                    <strong>Step ${index + 1}:</strong> Pick item ${step.item_id} at ${step.location}
                </div>
            `);
        });
        
        $('#route-summary').html(`
            Total estimated travel distance: ${routeData.total_distance.toFixed(2)} units
        `);
    }
    
    function drawRouteVisualization(route) {
        var canvas = document.getElementById('route-canvas');
        var ctx = canvas.getContext('2d');
        
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        if (route.length === 0) return;
        
        // Draw zones
        ctx.font = '12px Arial';
        for (const [zone, coords] of Object.entries({
            "ZONE_1": {x: 50, y: 50},
            "ZONE_2": {x: 300, y: 50},
            "ZONE_3": {x: 550, y: 50},
            "ZONE_4": {x: 50, y: 200},
            "ZONE_5": {x: 300, y: 200},
            "ZONE_6": {x: 550, y: 200}
        })) {
            ctx.fillStyle = '#ddd';
            ctx.fillRect(coords.x - 40, coords.y - 20, 80, 40);
            ctx.fillStyle = '#000';
            ctx.fillText(zone, coords.x - 30, coords.y + 5);
        }
        
        // Draw route
        ctx.beginPath();
        ctx.strokeStyle = '#4CAF50';
        ctx.lineWidth = 2;
        
        // Start at first point
        const start = route[0].coordinates;
        const adjustedStart = {
            x: (start.x / 200) * 500 + 50,
            y: (start.y / 100) * 150 + 50
        };
        ctx.moveTo(adjustedStart.x, adjustedStart.y);
        
        // Draw lines to each subsequent point
        for (let i = 1; i < route.length; i++) {
            const point = route[i].coordinates;
            const adjustedPoint = {
                x: (point.x / 200) * 500 + 50,
                y: (point.y / 100) * 150 + 50
            };
            ctx.lineTo(adjustedPoint.x, adjustedPoint.y);
        }
        ctx.stroke();
        
        // Draw points
        route.forEach((step, index) => {
            const point = step.coordinates;
            const adjustedPoint = {
                x: (point.x / 200) * 500 + 50,
                y: (point.y / 100) * 150 + 50
            };
            
            ctx.beginPath();
            ctx.fillStyle = index === 0 ? '#FF5722' : '#2196F3';
            ctx.arc(adjustedPoint.x, adjustedPoint.y, 6, 0, Math.PI * 2);
            ctx.fill();
            
            // Label points
            ctx.fillStyle = '#000';
            ctx.fillText(` ${step.item_id}`, adjustedPoint.x + 10, adjustedPoint.y + 5);
        });
    }
});