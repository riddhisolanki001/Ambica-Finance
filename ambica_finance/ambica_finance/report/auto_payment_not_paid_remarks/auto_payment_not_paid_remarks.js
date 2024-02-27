// Copyright (c) 2024, riddhi and contributors
// For license information, please see license.txt

// // Create a script element
// const script = document.createElement('script');

// // Set the source attribute to the CDN URL of the xlsx library
// script.src = 'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.17.3/xlsx.full.min.js';

// // Append the script element to the document's head
// document.head.appendChild(script);

// // Wait for the script to load
// script.onload = function() {
//     // Now you can use the XLSX object
//     console.log(XLSX);
// };




// function handleDownloadExcel(report) {

// 	let downloadCounter = localStorage.getItem('downloadCounter') || 1;

//     // const reportColumns = report.columns;
//     const reportData = report.data;
// 	console.log(report.data)
// 	if (reportData.length > 0) {
// 		// Combine report columns and data into one object
// 		const jsonData = [...reportData];

// 		// Convert JSON data to Excel format
// 		const workbook = XLSX.utils.book_new();
// 		const worksheet = XLSX.utils.json_to_sheet(jsonData);
// 		XLSX.utils.book_append_sheet(workbook, worksheet, "Sheet1");

// 		// Convert workbook to binary Excel format
// 		const excelData = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });

// 		// Convert binary Excel data to Blob
// 		const blob = new Blob([excelData], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });

// 		// Create download link
// 		const a = document.createElement('a');
// 		a.style.display = 'none';
// 		document.body.appendChild(a);

// 		if (downloadCounter > 1) {
// 			a.download = `auto_payment_not_paid_remarks_${downloadCounter}.xlsx`;
// 		} else {
// 			a.download = 'auto_payment_not_paid_remarks.xlsx';
// 		}

// 		// Set href attribute of download link
// 		a.href = window.URL.createObjectURL(blob);

// 		// Trigger click event to start downloading
// 		a.click();

// 		// Cleanup: remove download link from DOM
// 		document.body.removeChild(a);

// 		// Increment download counter for next file
// 		downloadCounter++;

// 		// Save updated counter value to localStorage
// 		localStorage.setItem('downloadCounter', downloadCounter);
// 	} else {
// 		frappe.msgprint(__('No data found in the report.'));
// 	}
// }

frappe.query_reports["Auto Payment not Paid Remarks"] = {
	"filters": [

	],
	// onload: (report) => {
	
	// 	report.page.add_inner_button(__("Download Excel"), function () {
	// 		// Call the function to handle the download
	// 		handleDownloadExcel(report);
	// 	});
	// }
};
