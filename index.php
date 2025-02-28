<?php
$servername = "localhost";
$username = "root";
$password = "";
$database = "news";

// Create connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Hit Counter Logic
$counter_file = "counter.txt";
if (!file_exists($counter_file)) {
    file_put_contents($counter_file, "0");
}
$hits = (int) file_get_contents($counter_file);
$hits++;
file_put_contents($counter_file, $hits);

// Default SQL query
$sql = "SELECT id, headline, link, summary, source, scrape_date FROM NewsArticles ORDER BY scrape_date DESC";

// Date filtering logic
if ($_SERVER["REQUEST_METHOD"] == "POST" && !empty($_POST["start_date"]) && !empty($_POST["end_date"])) {
    $start_date = $conn->real_escape_string($_POST["start_date"]);
    $end_date = $conn->real_escape_string($_POST["end_date"]);

    if (preg_match("/^\\d{4}-\\d{2}-\\d{2}$/", $start_date) && preg_match("/^\\d{4}-\\d{2}-\\d{2}$/", $end_date)) {
        $sql = "SELECT id, headline, link, summary, source, scrape_date FROM NewsArticles 
                WHERE scrape_date BETWEEN '$start_date' AND '$end_date' 
                ORDER BY scrape_date DESC";
    }
}

$result = $conn->query($sql);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cybersecurity News</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>

    <style>
        /* Banner */
        .banner {
            background: linear-gradient(135deg, #004aad, #00bcd4);
            color: white;
            height: 5cm;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
            font-family: 'Arial', sans-serif;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            margin: 20px;
            text-align: center;
        }

        .news-logo {
            width: 80px;
            height: auto;
        }

        .news-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            padding: 20px 0;
        }

        .news-card {
            background: white;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease-in-out, box-shadow 0.3s;
        }

        .news-card:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        }

        .btn-gradient {
            background: linear-gradient(90deg, #ff7eb3, #ff758c);
            color: white;
            border: none;
        }

        .btn-gradient:hover {
            background: linear-gradient(90deg, #ff758c, #ff7eb3);
        }

        /* Dark Mode */
        body.dark-mode {
            background: #121212;
            color: #ffffff;
            transition: background 0.5s, color 0.5s;
        }

        .dark-mode .banner {
            background: linear-gradient(135deg, #222, #444);
        }

        .dark-mode .news-card {
            background: #1e1e1e;
            color: #fff;
            box-shadow: 0 4px 8px rgba(255, 255, 255, 0.2);
        }

        .dark-mode .btn-gradient {
            background: linear-gradient(90deg, #ff7eb3, #ff758c);
        }

        /* Hide elements in print mode */
        @media print {
            .no-print {
                display: none !important;
            }
        }
    </style>
</head>
<body onload="updateTime()">

    <!-- Banner with Date, Time, and Hit Counter -->
    <div class="banner">
        <img src="news.png" alt="News Logo Left" class="news-logo">
        <div class="banner-text">
            <h1>Cyber News</h1>
            <!--<h2>Cyber News</h2>-->        
            <p>Latest updates on hacking, threats, and security trends</p>
            <p><strong>Date & Time: </strong><span id="dateTime"></span></p>
            <p><strong>Visitor Count: </strong> <?= $hits; ?> </p>
        </div>
        <img src="news.gif" alt="News Logo Right" class="news-logo">
    </div>

    <!-- Buttons -->
    <div class="container text-center mb-4 no-print">
        <button class="btn btn-dark me-2" onclick="toggleDarkMode()">
            <span id="darkModeIcon">🌙</span> Toggle Dark Mode
        </button>
        <button class="btn btn-gradient me-2" onclick="window.print()">🖨️ Print</button>
        <button class="btn btn-gradient" onclick="exportPDF()">📄 Export to PDF</button>
    </div>

    <!-- Filter Section -->
    <div class="container mt-4 no-print">
        <h2>Filter News by Date</h2>
        <form method="post" class="row g-3">
            <div class="col-md-4">
                <label for="start_date" class="form-label">Start Date:</label>
                <input type="date" id="start_date" name="start_date" class="form-control">
            </div>
            <div class="col-md-4">
                <label for="end_date" class="form-label">End Date:</label>
                <input type="date" id="end_date" name="end_date" class="form-control">
            </div>
            <div class="col-md-4 d-flex align-items-end">
                <button type="submit" class="btn btn-gradient w-100">Filter</button>
            </div>
        </form>
    </div>

    <div class="container mt-4">
        <h3>News Articles</h3>
        <div class="news-grid">
            <?php 
            if ($result->num_rows > 0): 
                while ($row = $result->fetch_assoc()): ?>
                    <div class="news-card">
                        <h5><?= htmlspecialchars($row['headline']) ?></h5>
                        <p><?= htmlspecialchars(substr($row['summary'], 0, 100)) ?>...</p>
                        <a href="<?= htmlspecialchars($row['link']) ?>" target="_blank">Read more</a>
                        <small>Source: <?= htmlspecialchars($row['source']) ?> | Date: <?= htmlspecialchars($row['scrape_date']) ?></small>
                    </div>
                <?php endwhile; ?>
            <?php else: ?>
                <p class="text-center">No news articles found</p>
            <?php endif; ?>
        </div>
    </div>

    <script>
        function exportPDF() {
            const { jsPDF } = window.jspdf;
            html2canvas(document.body, { scale: 2 }).then(canvas => {
                let pdf = new jsPDF('p', 'mm', 'a4');
                let imgData = canvas.toDataURL('image/png');
                pdf.addImage(imgData, 'PNG', 0, 0, 210, (canvas.height * 210) / canvas.width);
                pdf.save('cyber_news.pdf');
            });
        }

        function updateTime() {
            document.getElementById("dateTime").innerText = new Date().toLocaleString();
            setTimeout(updateTime, 1000);
        }

        function toggleDarkMode() {
            document.body.classList.toggle("dark-mode");
        }
    </script>

</body>
</html>

<?php $conn->close(); ?>
