frappe.query_reports["HSN Wise Inward Summery"] = {
    onload: (report) => {
        let downloadCounter = localStorage.getItem('downloadCounter') || 1;

        report.page.add_inner_button(__("Download JSON"), function () {
            const reportData = report.data;

            if (reportData.length > 0) {
                // Convert data to JSON
                const jsonData = JSON.stringify(reportData, null, 2);

                // Create a Blob containing the JSON data
                const blob = new Blob([jsonData], { type: 'application/json' });

                // Create a download link
                const a = document.createElement('a');

                if (downloadCounter > 1) {
                    a.download = `hsn_wise_inward_summary_${downloadCounter}.json`;
                } else {
                    a.download = 'hsn_wise_inward_summary.json';
                }

                // Trigger the click event
                a.href = window.URL.createObjectURL(blob);
                a.click();

                // Increment the download counter for the next file
                downloadCounter++;

                // Save the updated counter value to localStorage
                localStorage.setItem('downloadCounter', downloadCounter);
            } else {
                frappe.msgprint(__('No data found in the report.'));
            }
        });
    }
};
