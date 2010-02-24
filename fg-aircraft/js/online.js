Ext.onReady(function(){

var REFRESH_RATE = 5;
var refresh_counter = REFRESH_RATE;

function render_callsign(v, meta, rec){
	switch(rec.get('flag')){
		case 0: //* pilot is flying
			meta.css = 'fg_pilot_fly';
			break;
		case 1: //* pilot is new
			meta.css = 'fg_pilot_new';
			break;
		default: //* pilot is < 0 = delete timer
			meta.css = 'fg_pilot_dead';
			break;
	}
	return v;
}

function render_altitude(v, meta, rec, rowIdx, colIdx, store){
	if(v < 1000){
		color = '#931429';
	}else if(v < 2000){
		color = '#FA405F';
	}else if(v < 4000){
		color = '#CCFA40';
	}else if(v < 6000){
		color = '#7FFA40';
	}else if(v < 8000){
		color = '#40FA6E';
	}else if(v < 10000){
		color = '#40FAAA';
	}else if(v < 15000){
		color = '#FA405F';
	}else if(v < 20000){
		color = '#40FAFA';
	}else{
		color = '#331CDC';
	}
	return "<span style='color:" + color + ';">' + Ext.util.Format.number(v, '0,000'); + '</span>';
}


//********************************************************************************************
Ext.onReady(function(){

//****************************************************************

var pilotsSummaryCountLabel = new Ext.Toolbar.TextItem({text:'No pilots'});
var pilotsDataCountLabel = new Ext.Toolbar.TextItem({text:'No pilots'});

var refreshTimerLabel = new Ext.Toolbar.TextItem({text:'-'});

var PilotRecord = Ext.data.Record.create([
	{name: 'flag', type: 'int'},
	{name: "callsign", type: 'string'},
	{name: "server_ip", type: 'string'},
	{name: "model", type: 'string'},
	{name: "lat", type: 'float'},
	{name: "lng", type: 'float'},
	{name: "alt", type: 'int'},
	{name: "heading", type: 'string'},
	{name: "pitch", type: 'string'},
	{name: "roll", type: 'string'}
]);



//* list of pilot markers (atmo there is no ID etc in api3)
var pilotMarkers = {};

//* Pilots Datastore
var pilotsStore = new Ext.data.Store({
	fields: [ 	{name: 'flag', type: 'int'},
				{name: "callsign", type: 'string'},
				{name: "server_ip", type: 'string'},
				{name: "model", type: 'string'},
				{name: "lat", type: 'float'},
				{name: "lng", type: 'float'},
				{name: "alt", type: 'int'},
				{name: "heading", type: 'string'},
				{name: "pitch", type: 'string'},
				{name: "roll", type: 'string'}
	]
	//, sortInfo: {field: "callsign", direction: 'ASC'}
});
pilotsStore.on("exception", function(prx, typ, act){
	//TODO
	console.log("exception", prx, typ, act);
});


    

function load_pilots(){
	//console.log(refresh_counter);
	if(refresh_counter > 0){
		refresh_counter--;
		refreshTimerLabel.setText(refresh_counter);
		setTimeout(load_pilots, 1000);
		return
	}
	refreshTimerLabel.setText('loading')
	//console.log("AJAX pilots request -------------------------------------");
	Ext.Ajax.request({
		url: "/rpc/online/",
		method: 'GET',
		success: function(resp, opts){
			//console.log("ok", resp);
			var json = Ext.decode(resp.responseText);
			console.log("ok-pilots", json);
			var pilots =  json['data'];
		
			//* loop thru existing pilots and update
			if(pilotsStore.getCount() > 0){
				//for(var idx=0; idx <= pilotsStore.getCount(); idx++){
				pilotsStore.each( function(rec){	
					//var rec = pilotsStore.getAt(idx);
					if(rec){
						//console.log( rec.id);

						if(pilots[rec.id]){
							//* Pilot exists so update
							rec.set('flag', 0);
							rec.set('lat', pilots[rec.id].lat);
							rec.set('lng', pilots[rec.id].lng);
							rec.set('alt', pilots[rec.id].alt);
							rec.set('heading', pilots[rec.id].heading);
							rec.set('pitch', pilots[rec.id].pitch);
							rec.set('roll', pilots[rec.id].roll);
							delete pilots[rec.id]
						}else{
							var f = rec.get('flag');
							if(f > 0){
								rec.set('flag', -1);	
							}else{
								f = f -1;
								rec.set('flag', f);	
							}
							//console.log("dead", );
							
							//
						}
					}else{
						console.log("errOR");
					}
					/*
					if(pilots[rec.get('callsign')]){
						console.log("update", rec);
						rec.set('flag', 0);
					}else{
						console.log("exist", idx, rec);
						rec.set('flag', 2);
					} */
				}, this);
			}
			//* add new pilots_list
			for(var p in pilots){
				//console.log("add", p);
				pilots[p].flag = 1;
				var pRec = new PilotRecord(pilots[p], p);
				pilotsStore.add(pRec);
				delete pilots[p]
			}
			//* Update count labels
			var cnt = pilotsStore.getCount();
			//console.log("cnt", cnt, "pilots.length", pilots);
			var lbl = cnt == 0 ? "No Pilots Online" : cnt + " Pilots Online"
			pilotsSummaryCountLabel.setText(lbl);
			pilotsDataCountLabel.setText(lbl);
			refreshTimerLabel.setText(refresh_counter)
			refresh_counter = REFRESH_RATE;
			setTimeout(load_pilots, 1000);
		},
		failure: function(resp, opts){
			//TODO error handler
			console.log("fail");
			refreshTimerLabel.setText("Failed")
			refresh_counter = REFRESH_RATE;
			setTimeout(load_pilots, 1000);
		}
	});

}

        
var grid = new Ext.grid.GridPanel({
	title: 'Pilots Online',
	//iconCls: 'iconPilots',
	autoScroll: true,
	autoWidth: true,
	hideTitle: true,
	height: 600,
	renderTo: 'online_grid',
	//tbar:[  mapToolBarItems//this.actionAdd, this.actionEdit, this.actionDelete, 
			//'-',// this.actionLabSelectToolbarButton,
			//'->',
			//Geo2.widgets.goto_www('Online', 'View rates on website', '/rates.php'),
		//	{text: 'Refresh', iconCls: 'iconRefresh', handler: function(){
				//load_pilots();
				//}
			//}    
	//],
	tbar: [],
	viewConfig: {emptyText: 'No pilots online', forceFit: true}, 
	//sm: this.selModel,
	store: pilotsStore,
	loadMask: true,
	columns: [  //this.selModel,	
		{header: 'F',  dataIndex:'flag', sortable: true, width: 20},
		{header: 'CallSign',  dataIndex:'callsign', sortable: true, renderer: render_callsign},
		{header: 'Aircraft',  dataIndex:'model', sortable: true},
		{header: 'Lat', dataIndex:'lat', sortable: true, align: 'right',
			renderer: function(v, meta, rec, rowIdx, colIdx, store){
				return Ext.util.Format.number(v, '0.000');
			}
		},
		{header: 'Lng', dataIndex:'lng', sortable: true, align: 'right',
			renderer: function(v, meta, rec, rowIdx, colIdx, store){
				return Ext.util.Format.number(v, '0.000');
			}
		},
		{header: 'Alt', dataIndex:'alt', sortable: true, align: 'right',
			renderer: render_altitude
		},
		{header: 'Heading', dataIndex:'heading', sortable: true, align: 'right',
			renderer: function(v, meta, rec, rowIdx, colIdx, store){
				return Ext.util.Format.number(v, '0');
			}
		},
		{header: 'Pitch', dataIndex:'pitch', sortable: true, align: 'right',
			renderer: function(v, meta, rec, rowIdx, colIdx, store){
				return Ext.util.Format.number(v, '0');
			}
		},
		{header: 'Roll', dataIndex:'roll', sortable: true, align: 'right',
			renderer: function(v, meta, rec, rowIdx, colIdx, store){
				return Ext.util.Format.number(v, '0');
			}
		},
		{header: 'Server', dataIndex:'server_ip', sortable: true, align: 'left',
			renderer: function(v, meta, rec, rowIdx, colIdx, store){
				return v;
			}
		}

	],
	listeners: {},
	bbar: [pilotsDataCountLabel]
});
	load_pilots();
});


	
}); /* Ext.onready() */

