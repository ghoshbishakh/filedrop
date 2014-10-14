package com.binayak.filedrop;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;


public class MainActivity extends Activity
{
	public static class socketContainer {
		public Socket s1;
		public String ipAddress = "192.168.43.212";
		public int port = 55667;
	}
	
	private static socketContainer soc;
	
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        if(savedInstanceState == null){
        	soc = new socketContainer();
        	// Start the listener
        	
        	/*
        	 * Creates a new Intent to start the RSSPullService
        	 * IntentService. Passes a URI in the
        	 * Intent's "data" field.
        	 */
        	Intent mServiceIntent = new Intent(this, ListenerService.class);
        	mServiceIntent.setData(Uri.parse(dataUrl));
            this.startService(mServiceIntent);
        	

        	/*TextView mText = (TextView) findViewById(R.id.text_id);
        	Log.i("Main", "starting listner..");
        	new listenTask(soc, mText).execute(1);
        	Log.i("Main", "listner started.");*/
        }
    }

    public void shout(View view){        
        EditText editText = (EditText) findViewById(R.id.edit_message);
        String message = editText.getText().toString();
        Log.i("Main", "Starting shout task..");
        new shoutTask(soc).execute(message);
    }
    
    // Asyn task to listen to socket
    private class listenTask extends AsyncTask<Integer, String, String> {
        private socketContainer mSoc;
        private TextView mTextview;
        public listenTask(socketContainer soc, TextView tv){
            mSoc = soc;
            mTextview = tv;
        }

        @Override
        protected String doInBackground(Integer... n) {
        	Log.i("Listener", "Started.");
            char c;
            String msg = "";
            try {
                if(mSoc.s1 == null){
                    try{
                        mSoc.s1 = new Socket(mSoc.ipAddress, mSoc.port); 
                        Log.i("Listener", "Connection created.");
                    }
                    catch(IOException e){
                        Log.e("Connection Failed", "" +e);
                    }
                }

                InputStream in = null;
                while(mSoc.s1.isConnected()){
                	if (in == null){
                		in = mSoc.s1.getInputStream();
                	}
                
                	while(in.available() > 5){
                		Log.d("Listener", "" + in.available());
                		c= (char)in.read();
                		msg += c;
                		if (c == '\n'){
                    		Log.i("Listener", "" + in.available());
                			break;
                		}
                	}
                	if (msg != ""){
                		Log.i("Listner", msg);
                		msg = "";
                	}
                }
            }
            catch(IOException e){
                Log.e("shoutTask", "Failed to send message: " + e);
            }
            return "Connection closed.";
        }
        
        @Override
        protected void onProgressUpdate(String... msg){
        	
        }
        
        @Override
        protected void onPostExecute(String msg) {
            Log.i("listenTask", "Stoppe: " + msg);
        }
    }
    
    // Async Task to send messages
    private class shoutTask extends AsyncTask<String, Void, String> {
        private socketContainer mSoc;
        public shoutTask(socketContainer soc){
            mSoc = soc;
        }

        @Override
        protected String doInBackground(String... msg) {
        	Log.i("shoutTask", "started.");
            try {
                if(mSoc.s1 == null){
                	Log.i("shoutTask", "trying to create socket");
                    try{
                        mSoc.s1 = new Socket(mSoc.ipAddress, mSoc.port);  
                        Log.i("shoutTask", "Connection created.");                          
                    }
                    catch(IOException e){
                        Log.e("Connection Failed", "" +e);
                    }
                }
                Log.i("shoutTask", "trying to shout.");
                OutputStream out = mSoc.s1.getOutputStream();
                out.write(msg[0].getBytes());
                out.write("\r\n".getBytes());
                out.flush();               
            }
            catch(IOException e){
                Log.e("shoutTask", "Failed to send message: " + e);
            }
            return "Done.";
        }
        
        @Override
        protected void onPostExecute(String msg) {
            Log.i("shoutTask", "Successfully sent message." + msg);
        }
    }
}
