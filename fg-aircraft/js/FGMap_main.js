var FG = {};
FG.map = {};
FG.pilots_list = {};

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
var latLabel = new Ext.Toolbar.TextItem({text:'Lat: -0.00'});
var lngLabel = new Ext.Toolbar.TextItem({text:'Lng: -0.00'});

var pilotsSummaryCountLabel = new Ext.Toolbar.TextItem({text:'No pilots'});
var pilotsDataCountLabel = new Ext.Toolbar.TextItem({text:'No pilots'});

var refreshTimerLabel = new Ext.Toolbar.TextItem({text:'-'});


var mapToolBarItems = new Array();
var ranges = [{zoom: 4, caption: '10km'},{zoom: 9, caption: '20km'},  {zoom: 11, caption: '100km'}];
for(var r in ranges){
	mapToolBarItems.push({text: ranges[r].caption, gr_zoom: ranges[r].zoom});
}
mapToolBarItems.push({text: 'VOR', iconCls: 'iconVor'});
mapToolBarItems.push({text: 'ADF', iconCls: 'iconAdf'});
mapToolBarItems.push(latLabel);
mapToolBarItems.push(lngLabel);


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
		url: "rpc/pilots_online",
		method: 'GET',
		success: function(resp, opts){
			//console.log("ok", resp);
			var json = Ext.decode(resp.responseText);
			console.log("ok-pilots", json);
			var pilots =  json['pilots'];
		
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

//LATER
//var pilotsSelectionModel = new Ext.grid.CheckboxSelectionModel({singleSelect:false});

// NOTE: This is an example showing simple state management. During development,
// it is generally best to disable state management as dynamically-generated ids
// can change across page loads, leading to unpredictable results.  The developer
// should ensure that stable state ids are set for stateful components in real apps.
//TODO - sense LOCAL_DEV env
// uncommnet below for production 
//Ext.state.Manager.setProvider(new Ext.state.CookieProvider());

        
var viewport = new Ext.Viewport({
	layout: 'border',
	plain: true,
	items: [
		//** Left/West area
		{title: 'FlightGear Map <small>v0.1-experimental</small>', region: 'west',
			split: true,
			width: 300,
			minSize: 175,
			maxSize: 400,
			collapsible: true,
			margins: '0 0 0 5',
			layout: {
				type: 'fit'
			},
			items: new Ext.TabPanel({
				activeTab: 0,
				items: [
					//**** Pilots Lookup Grid
					new Ext.grid.GridPanel({
						title: 'Pilots',
						iconCls: 'iconPilots',
						autoScroll: true,
						autoWidth: true,
						tbar:[  //this.actionAdd, this.actionEdit, this.actionDelete, 
								'-',// this.actionLabSelectToolbarButton,
								'->',
								//Geo2.widgets.goto_www('Online', 'View rates on website', '/rates.php'),
								{text: 'Refresh', iconCls: 'iconRefresh', handler: function(){
									//pilotsStore.reload();
									load_pilots();
									}
								}    
						],
						viewConfig: {emptyText: 'No pilots online', forceFit: true}, 
						//sm: this.selModel,
						store: pilotsStore,
						loadMask: true,
						//TODO sm: pilotsSelectionModel,
						columns: [  //TODO pilotsSelectionModel,
									{header: 'CallSign',  dataIndex:'callsign', sortable: true, renderer: render_callsign},
									{header: 'Aircraft',  dataIndex:'model', sortable: true}
						],
						listeners: {},
						bbar: [pilotsSummaryCountLabel, '->', refreshTimerLabel]
					}),
					//**** Navigation Widget
					{
					title: 'Navigation',
					iconCls: 'iconNav',
					html: '<p>Some settings in here.</p>',
					border: false
					}
				]
			   }) // end tabpanel
            },
            // in this instance the TabPanel is not wrapped by another panel
            // since no title is needed, this Panel is added directly
            // as a Container
           //* src="http://mpmap01.flightgear.org/mpstatus/"
            new Ext.TabPanel({
                region: 'center', // a center region is ALWAYS required for border layout
                deferredRender: false,
                activeTab: 0,
				border: 0,
                items: [
					new Ext.Panel(
					{
						contentEl: 'map_canvas',
						title: 'Map&nbsp;&nbsp;',
						iconCls: 'iconMap',
						tbar: mapToolBarItems,
						autoScroll: true
					}),
					//***************************************************
					//**** Pilots Main Grid
					new Ext.grid.GridPanel({
						title: 'Pilots Data',
						iconCls: 'iconPilots',
						autoScroll: true,
						autoWidth: true,
						//tbar:[  mapToolBarItems//this.actionAdd, this.actionEdit, this.actionDelete, 
								//'-',// this.actionLabSelectToolbarButton,
								//'->',
								//Geo2.widgets.goto_www('Online', 'View rates on website', '/rates.php'),
							//	{text: 'Refresh', iconCls: 'iconRefresh', handler: function(){
									//load_pilots();
									//}
								//}    
						//],
						tbar: mapToolBarItems,
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
					}),
				//** Server Status
				{
                    contentEl: 'center2',
                    title: 'Servers Status',
					iconCls: 'iconServerStatus',
                    autoScroll: true
                }
				]
            })]
        });


map_initialize();
load_pilots();
}); /* Ext.onready() */

