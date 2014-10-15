package com.binayak.filedrop;

import android.app.IntentService;
import android.content.Intent;

public class ListenerService extends IntentService {
    public ListenerService(String name) {
		super(name);
		// TODO Auto-generated constructor stub
	}

	@Override
    protected void onHandleIntent(Intent workIntent) {
        // Gets data from the incoming Intent
        String dataString = workIntent.getDataString();
        
    }
}