// Copyright (c) 2024, riddhi and contributors
// For license information, please see license.txt

frappe.query_reports["NEFT RTGS"] = {
	filters: [],
    onload: function(report) {
        $('[data-label="Export"]').parent().hide();
        report.page.add_inner_button(__('Export File'), function() {
            exportHSNWiseSummaryCsv();
        });
    }
};


function exportHSNWiseSummaryCsv() {
    // Fetch HSN Wise Summary data
    fetchHSNWiseSummaryData(function (hsnData) {
        if (hsnData && hsnData.length > 0) {
            // Prepare CSV content
            var csvContent = "";

            // Add header row
            csvContent += Object.keys(hsnData[0]).join(",") + "\n";

            // Add data rows
            hsnData.forEach(function (row) {
                var values = Object.values(row);
                csvContent += values.join(",") + "\n";
            });

            // Remove the first row (header) from CSV content
            csvContent = csvContent.split('\n').slice(1).join('\n');

            // Create a Blob with the CSV content
            var blob = new Blob([csvContent], { type: "text/csv" });

            // Create a link element and trigger a click to download the file
            var link = document.createElement("a");
            link.href = window.URL.createObjectURL(blob);
            link.download = "neft_rtgs.csv";
            link.click();
        } else {
            console.error("Failed to fetch HSN Wise Summary data.");
        }
    });
}

function fetchHSNWiseSummaryData(callback) {
    // Fetch data from the report API endpoint or use your custom method to fetch data
    // Adjust the URL accordingly based on your Frappe application structure
    var apiUrl = "/api/method/frappe.desk.query_report.run";
    var reportName = "NEFT RTGS";

    frappe.call({
        method: "frappe.desk.query_report.run",
        args: {
            report_name: reportName,
            filters: {},
        },
        callback: function (response) {
            if (response.message && response.message.result) {
                // If the data is successfully fetched, pass it to the callback
                callback(response.message.result);
            } else {
                // Handle error
                console.error("Failed to fetch HSN Wise Summary data.");
                callback(null);
            }
        },
    });
}
