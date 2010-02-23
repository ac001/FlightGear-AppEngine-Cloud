
var visibles = {};

function toggle_layer(id){
		//#	var obj = document.getElementById(id)
			//#em.style.visibility = "hidden"
	//#return
	var cmp = Ext.get(id);
	if(visibles[id]){
		cmp.slideOut();
		delete visibles[id]
		//#obj.style.visibility = "hidden";

	}else{
		cmp.slideIn();
		visibles[id] = true;
		//#obj.style.visibility = "visible"
	}

}


function search_aero(aero){
    Ext.Ajax.Request({
        url: '/rpc/aircraft/',
		method: 'GET',
		success: function(){

		},

		failure: function(){

		}

	});
}

