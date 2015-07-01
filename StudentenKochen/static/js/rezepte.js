$(document).ready(function() {
	var addButton = $('#addButton');
	var addBox = $('#addBox');
	var addBoxq= $('#addBoxq')
	var countBox =2;
	
	addButton.click(function() 	{
		var quantity ="quantity" + countBox; 
		var ingredient="ingredient" + countBox; 
		
	    $('<input type="text" name="'+quantity+'" style="width:50px; margin-right:17px;" />').appendTo(addBoxq);
		$('<input type="text" name="'+ingredient+'" style="width:100px;" /><br />').appendTo(addBoxq)
	    countBox += 1;
	});
});