
function OnlineWidget(){

var self = this;
this.REFRESH_RATE = 5;
this.refresh_counter = 0;

this.render_callsign = function(v, meta, rec){
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

this.render_altitude = function(v, meta, rec, rowIdx, colIdx, store){
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

//this.pilotsSummaryCountLabel = new Ext.Toolbar.TextItem({text:'No pilots'});
this.pilotsDataCountLabel = new Ext.Toolbar.TextItem({text:'No pilots'});

this.refreshTimerLabel = new Ext.Toolbar.TextItem({text:'-'});

this.PilotRecord = Ext.data.Record.create([
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

//* Pilots Datastore
this.pilotsStore = new Ext.data.JsonStore({
	url: "/rpc/online/",
	method: 'GET',
	root: 'data',
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
this.pilotsStore.on("exception", function(prx, typ, act){
	//TODO
	//console.log("exception", prx, typ, act);
});
this.pilotsStore.on("load", function(){
	//TODO
	//console.log("exception", prx, typ, act);
	setTimeout(self.step_counter, 1000);
});

this.step_counter = function(){
	self.refresh_counter++;
	self.refreshTimerLabel.setText(self.refresh_counter);
	setTimeout(self.step_counter, 1000);
}

    

this.load_pilots = function(){
	//this.pilotsStore.load()
	//return
	//console.log(refresh_counter);
	if(self.refresh_counter > 0){
		self.refresh_counter--;
		self.refreshTimerLabel.setText(self.refresh_counter);
		setTimeout(self.load_pilots, 1000);
		return
	}
	self.refreshTimerLabel.setText('loading');
	//console.log("AJAX pilots request -------------------------------------");
	Ext.Ajax.request({
		url: "/rpc/online/",
		method: 'GET',
		success: function(resp, opts){
			//console.log("ok", resp);
			var json = Ext.decode(resp.responseText);
			//console.log("ok-pilots", json);
			var pilots =  json['data'];
		
			//* loop thru existing pilots and update
			if(self.pilotsStore.getCount() > 0){
				//for(var idx=0; idx <= pilotsStore.getCount(); idx++){
				self.pilotsStore.each( function(rec){	
					//var rec = pilotsStore.getAt(idx);
					if(rec){
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
							}
					}else{
						//console.log("errOR");
					}
				}, this);
			}
			//* add new pilots_list
			for(var p in pilots){
				//console.log("add", p);
				pilots[p].flag = 1;
				var pRec = new self.PilotRecord(pilots[p], p);
				self.pilotsStore.add(pRec);
				delete pilots[p]
			}
			//* Update count labels
			var cnt = self.pilotsStore.getCount();
			//console.log("cnt", cnt, "pilots.length", pilots);
			var lbl = cnt == 0 ? "No Pilots Online" : cnt + " Pilots Online"
			self.grid.setTitle(lbl);
			self.pilotsDataCountLabel.setText(lbl);
			self.refresh_counter = self.REFRESH_RATE;
			self.refreshTimerLabel.setText(self.refresh_counter)
			setTimeout(self.load_pilots, 1000);
		},
		failure: function(resp, opts){
			//TODO error handler
			//console.log("fail");
			self.refreshTimerLabel.setText("Failed")
			self.refresh_counter = self.REFRESH_RATE;
			setTimeout(self.load_pilots, 1000);
		}
	});

} /* load pilots */

        
this.grid = new Ext.grid.GridPanel({
	title: 'Pilots Online',
	//iconCls: 'iconPilots',
	autoScroll: true,
	autoWidth: true,
	height: 600,
	renderTo: 'online_grid',
	viewConfig: {emptyText: 'No pilots online', forceFit: true}, 
	//sm: this.selModel,
	store: this.pilotsStore,
	loadMask: true,
	columns: [  //this.selModel,	
		{header: 'F',  dataIndex:'flag', sortable: true, width: 20},
		{header: 'CallSign',  dataIndex:'callsign', sortable: true, 
			renderer: this.render_callsign
		},
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
			renderer: this.render_altitude
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
	bbar: [ self.refreshTimerLabel,
			'->',
			{text: 'Refresh Now', iconCls: 'iconRefresh', 
				handler: function(){
					self.load_pilots();
				}
			}    
	]
}); /* grid */



} /* OnlineWidget */

Ext.onReady(function(){

var widget = new OnlineWidget();
widget.load_pilots();
	
}); /* Ext.onready() */

