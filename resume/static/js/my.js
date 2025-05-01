        // Example starter JavaScript for disabling form submissions if there are invalid fields
(function() {
  'use strict';
  window.addEventListener('load', function() {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        // Always prevent the default form submission to avoid page reload
        event.preventDefault();
        event.stopPropagation();
        
        if (form.checkValidity() === false) {
          // Form is invalid, show validation errors
          form.classList.add('was-validated');
        } else {
          // Form is valid, process the data
          setdata();
          // Close the popup after data is set, but without hiding the header
          window.location.hash = "";
          
          // Ensure the header is visible
          document.getElementById('head').style.display = 'block';
        }
        
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();

function setdata(){
    // Set all the resume data from form values
    document.getElementById('uname').innerText = document.getElementById('name').value;
    document.getElementById('name_declaration').innerText = document.getElementById('name').value;
    document.getElementById('n_declaration').innerText = document.getElementById('name').value;
    
    document.getElementById('udob').innerText = document.getElementById('dob').value;
    document.getElementById('uphnum').innerText = document.getElementById('phnum').value;
    document.getElementById('uemail').innerText = document.getElementById('email').value;
    document.getElementById('ulocation').innerText = document.getElementById('city').value +", "+ document.getElementById('state').value;
    document.getElementById('dec_place').innerText = document.getElementById('city').value +", "+ document.getElementById('state').value;

    document.getElementById('uabout').innerText = document.getElementById('uaboutself').value;
    document.getElementById('ucareerobject').innerText = document.getElementById('ucareerob').value;

    document.getElementById('fathername').innerHTML = "Father's Name  <span style='margin-left:20px'></span>"+ ":" + document.getElementById('fname').value;
    document.getElementById('mothername').innerHTML = "Mother's Name   <span style='margin-left:20px'></span>"+":" + document.getElementById('mname').value;
    document.getElementById('permanentaddress').innerHTML = "Permanent Address    <span style='margin-left:20px'></span>"+":"+ document.getElementById('paddress').value;

    var myTab = document.getElementById('education_data');

    document.getElementById('education_data_table').innerHTML="";
    // LOOP THROUGH EACH ROW OF THE TABLE AFTER HEADER.
    for (i = 0; i < myTab.rows.length; i++) {
        // GET THE CELLS COLLECTION OF THE CURRENT ROW.
        var objCells = myTab.rows.item(i).cells;
        // LOOP THROUGH EACH CELL OF THE CURENT ROW TO READ CELL VALUES.
        var data = "<tr><td><span style='font-weight: 600;font-size: 20px'>"+
                objCells.item(0).innerHTML
                +"</span> <br>"+objCells.item(1).innerHTML+"</td>"+
                "<td>Graduated, "+objCells.item(2).innerHTML +" "+objCells.item(3).innerHTML+"</td></tr>";
        document.getElementById('education_data_table').innerHTML = document.getElementById('education_data_table').innerHTML + data;
    }

    var myTab = document.getElementById('acheivement_data');

    document.getElementById('achivements_data_li').innerHTML="";
    // LOOP THROUGH EACH ROW OF THE TABLE AFTER HEADER.
    for (i = 0; i < myTab.rows.length; i++) {
        // GET THE CELLS COLLECTION OF THE CURRENT ROW.
        var objCells = myTab.rows.item(i).cells;
        // LOOP THROUGH EACH CELL OF THE CURENT ROW TO READ CELL VALUES.
        
        var data = "<li style='font-size:18px;margin-bottom: 5px'>"+
                objCells.item(0).innerHTML + "</li>";
        document.getElementById('achivements_data_li').innerHTML = document.getElementById('achivements_data_li').innerHTML + data;
    }

    var myTab = document.getElementById('skill_data');

    document.getElementById('skills_data_li').innerHTML="";
    // LOOP THROUGH EACH ROW OF THE TABLE AFTER HEADER.
    for (i = 0; i < myTab.rows.length; i++) {
        // GET THE CELLS COLLECTION OF THE CURRENT ROW.
        var objCells = myTab.rows.item(i).cells;
        // LOOP THROUGH EACH CELL OF THE CURENT ROW TO READ CELL VALUES.
        
        var data = "<li style='font-size:18px;margin-bottom: 5px'>"+
                objCells.item(0).innerHTML + "</li>";
        document.getElementById('skills_data_li').innerHTML = document.getElementById('skills_data_li').innerHTML + data;
    }
}

// Simple PDF generation functions without jQuery dependencies to avoid conflicts
function printDiv() {
    var header = document.getElementById('head');
    if (header) header.style.display = 'none';
    
    setTimeout(function() {
        var element = document.getElementById('resume_1');
        if (!element) {
            if (header) header.style.display = 'block';
            alert("Error: Cannot find resume content.");
            return;
        }
        
        var opt = {
            margin: 0,
            filename: 'resume.pdf',
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2 },
            jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
        };
        
        html2pdf().from(element).set(opt).save().then(function() {
            if (header) header.style.display = 'block';
        }).catch(function(error) {
            console.error("PDF generation error:", error);
            if (header) header.style.display = 'block';
            alert("Error generating PDF. Please try again.");
        });
    }, 100);
}

function printDiv2() {
    var header = document.getElementById('head');
    if (header) header.style.display = 'none';
    
    setTimeout(function() {
        var element = document.getElementById('resume_2');
        if (!element) {
            if (header) header.style.display = 'block';
            alert("Error: Cannot find resume content.");
            return;
        }
        
        var opt = {
            margin: 0,
            filename: 'resume.pdf',
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2 },
            jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
        };
        
        html2pdf().from(element).set(opt).save().then(function() {
            if (header) header.style.display = 'block';
        }).catch(function(error) {
            console.error("PDF generation error:", error);
            if (header) header.style.display = 'block';
            alert("Error generating PDF. Please try again.");
        });
    }, 100);
}

// Helper functions for adding education, achievements, and skills
function addcourse(){
    if(document.getElementById('course').value == ""){
        document.getElementById('co_err').style.display="";
    }
    else if(document.getElementById('college').value == ""){
        document.getElementById('col_err').style.display="";
    }
    else if(document.getElementById('month').value == "Please select One.."){
        document.getElementById('select_month_err').style.display="";
    }
    else if(document.getElementById('year').value == "" || (document.getElementById('year').value) < 1990 || (document.getElementById('year').value) > 2060 ){
        document.getElementById('year_err').style.display="";
    }
    else{
        var table = document.getElementById("education_data");
        var row = table.insertRow(0);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);
        cell1.innerHTML = document.getElementById('course').value;
        cell2.innerHTML = document.getElementById('college').value;
        cell3.innerHTML = document.getElementById('month').value +" "+document.getElementById('year').value;
        cell4.innerHTML = "<input type='button' value='Delete' onclick='deleteRow(this)'";
    }
}

function addache(){
    if(document.getElementById('achivement').value==""){
        document.getElementById('achivement_err').style.display="";
    }
    else{
        var table = document.getElementById("acheivement_data");
        var row = table.insertRow(0);
        var cell1 = row.insertCell(0);
        cell1.innerHTML = document.getElementById('achivement').value;
    }
}

function achivementDeleteFunction() {
    document.getElementById("acheivement_data").deleteRow(0);
}

function addskills(){
    if(document.getElementById('skills').value==""){
        document.getElementById('skills_err').style.display="";
    }
    else{
        var table = document.getElementById("skill_data");
        var row = table.insertRow(0);
        var cell1 = row.insertCell(0);
        cell1.innerHTML = document.getElementById('skills').value;
    }
}

function skillsDeleteFunction() {
    document.getElementById("skill_data").deleteRow(0);
}

function myDeleteFunction() {
    document.getElementById("education_data").deleteRow(0);
}

// Add event listeners when the document is ready
$(document).ready(function() {
    console.log("Document ready, setting up button handlers");
    
    // Add event listener for resume 1 download button
    $('#download-pdf-1').on('click', function(e) {
        console.log("Download PDF button clicked for resume 1");
        e.preventDefault();
        printDiv();
    });
    
    // Add event listener for resume 2 download button
    $('#download-pdf-2').on('click', function(e) {
        console.log("Download PDF button clicked for resume 2");
        e.preventDefault();
        printDiv2();
    });
    
    // Legacy function support - still keep these for backwards compatibility
    window.printDiv = function() {
        console.log("printDiv called for resume_1");
        printDiv();
    };
    
    window.printDiv2 = function() {
        console.log("printDiv2 called for resume_2");
        printDiv2();
    };
});