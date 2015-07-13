
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
		
			var name = data.list[i].n;
			var image = data.list[i].i;
			var stream = data.list[i].s;
			
			
			var item = $("#t").clone();
			var id = "item" + n;
			item.prop("id",id);
			$(item).data("item",n);
			$(item).find(".caption").html(name);
			$(item).find(".thumbwrapper > img").prop("src",image);
			$(item).bind("click",function() {
				$.ajax({url:"/play/" + $(this).data("item")}).done(function(res) {
					procState(res);
				});
			});
			
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
