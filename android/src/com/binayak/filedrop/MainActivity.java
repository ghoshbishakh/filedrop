package com.binayak.filedrop;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

import android.app.Activity;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;


public class MainActivity extends Activity
{
	public static class socketContainer {
		public Socket sread;
		public Socket swrite;
		public String ipAddress = "192.168.1.4";
		public int port = 55667;
	}
	
	private static socketContainer soc;
	private static AsyncTask mlisten;
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        if(savedInstanceState == null){
        	soc = new socketContainer();
        	// Start the listener
        	Log.i("Main", "starting listner..");
        	mlisten = new listenTask(soc).execute(1);
        	Log.i("Main", "listner started.");
        }
    }

    @Override 
    protected void onStop(){
        super.onStop();
        try {
            soc.sread.close();
        }
        catch(IOException e){
            Log.i("Stopping", "socket already closed.");
        }
        mlisten.cancel(true);
    }
    
    public void updateTextView(String msg){            
            TextView mText = (TextView) findViewById(R.id.text_id);
            String message = mText.getText().toString() ;
            message += msg;
            mText.setText(message);
    }

    public void shout(View view){
        EditText editText = (EditText) findViewById(R.id.edit_message);
        final String msg = editText.getText().toString();
        editText.setText("");
	    new Thread(new Runnable() {
	        public void run() {
	        	Log.i("shoutTask", "started.");
	            try {
	                if(soc.sread == null){
	                	Log.i("shoutTask", "trying to create socket");
	                    try{
	                        soc.sread = new Socket(soc.ipAddress, soc.port);  
	                        Log.i("shoutTask", "Connection created.");                          
	                    }
	                    catch(IOException e){
	                        Log.e("Connection Failed", "" +e);
	                    }
	                }
	                Log.i("shoutTask", "trying to shout.");
	                OutputStream out = soc.sread.getOutputStream();
	                out.write(msg.getBytes());
	                out.write("\r\n".getBytes());
	                out.flush();
	                Log.i("shoutTask", msg);
	            }
	            catch(IOException e){
	                Log.e("shoutTask", "Failed to send message: " + e);
	            }
	        }
	   }).start();
    }
    
    // Asyn task to listen to socket
    private class listenTask extends AsyncTask<Integer, String, String> {
        private socketContainer mSoc;
        public listenTask(socketContainer soc){
            mSoc = soc;
        }

        @Override
        protected String doInBackground(Integer... n) {
        	Log.i("Listener", "Started.");
            char c;
            String msg = "";
            try {
                if(mSoc.sread == null){
                    try{
                        mSoc.sread = new Socket(mSoc.ipAddress, mSoc.port); 
                        Log.i("Listener", "Connection created.");
                    }
                    catch(IOException e){
                        Log.e("Connection Failed", "" +e);
                    }
                }

                InputStream in = null;
                while(mSoc.sread.isConnected()){
                	if (in == null){
                		in = mSoc.sread.getInputStream();
                	}
                
                	while(in.available() > 1){
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
                        publishProgress(msg);
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
        	updateTextView(msg[0]);
        }
        
        @Override
        protected void onPostExecute(String msg) {
            Log.i("listenTask", "Stoppe: " + msg);
        }
    }
}
