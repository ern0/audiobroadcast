
	$(document).ready(function() { 	

		$.ajax({
			url: "/list"
		}).done(function(data) {
			genList(data);
			procState(data);
		}).fail(function(e) {
			alert("playlist fail");
		});

		refreshState();

	});
	
	
	function refreshState() {

		$.ajax({
			url: "/state"
		}).done(function(res) {
			procState(res);
			setTimeout(refreshState,1000);
		}).fail(function(e) {
			setTimeout(refreshState,3000);
		});
	
	} // refreshState()
	

	function genList(data) {
	
		var n = 1;
		for (i in data.list) {
		
			var token = data.list[i].n;
			var name = token;
			token = token.toLowerCase()
			if (name[0] == "_") name.substring(1);
			var image = data.list[i].i;
			var stream = data.list[i].s;
			
			var item = $("#t").clone();
			var id = "item" + n;
			item.prop("id",id);
			$(item).data("item",n);
			$(item).find(".caption").html(name);
			$(item).find(".thumbwrapper > img").prop("src",image);
			
			if (token == "_youtube") {

				$(item).find(".caption").hide();
				$(item).find(".input").show().html('<input type="text" class="url" /><input value="go" class="go" type="submit"/>');
				
				$(item).find(".input").on("keyup",function(event) {
					if (event.keyCode == 13) $(this).find(".go").trigger("click");
				});
				
				$(item).find(".go").on("click",function() {
					url = $(this).parent().find(".url").val();
					$.ajax({url:"/youtube/" + url}).done(function(res) {
						procState(res);
					});
				});

			} else {
			
				$(item).find(".input").hide();
				$(item).find(".caption").show();
				$(item).bind("click",function() {
					$.ajax({url:"/play/" + $(this).data("item")}).done(function(res) {
						procState(res);
					});
				});
				
			}
			
			$("#list").append(item);
			item.show();
			n++;
			
		} // foreach item
	
	} // genList()


	function stop() {
		$.ajax({url:"/stop"}).done(function(res) {
			procState(res);
		});	
	}


	function procState(res) {
		//console.log(res.result,res.current);
		
		$("a").css("background","");
		if (res.current == -1) return;
		$("#item" + res.current).find("a").css("background","#dddddd");
	}
