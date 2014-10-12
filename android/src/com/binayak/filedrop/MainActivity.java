package com.binayak.filedrop;

import android.app.Activity;
import android.os.Bundle;

public class MainActivity extends Activity
{
	private Socket s1;
	private String ipAddress;
	private int port = 55667;
	private String msg = "";

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
    }

    public void connectToSocket(View view) {
        EditText editText = (EditText) findViewById(R.id.edit_message);
        ipAddress = editText.getText().toString();
    }

    public void sendMessage(View view) {

    }

    public void appendText(String s) {
    	this.msg += s;
    	this.msg += "\n";
    }

    // Async task to connect to socket
    private class downloadImageTask extends AsyncTask<String, Void, Bitmap> {
        private final WeakReference<ImageView> imageViewReference;
        private final ProgressBar progress;
        public downloadImageTask(ImageView mImageView, ProgressBar progress) {
            imageViewReference = new WeakReference<ImageView>(mImageView);
            this.progress = progress;
        }

        @Override
        protected Bitmap doInBackground(String... url) {
            return downloadImage(url[0]);
        }

        @Override
        protected void onPostExecute(Bitmap result) {
            ImageView mImageView = imageViewReference.get();
            mImageView.setImageBitmap(result);            
            // Set the text view as the activity layout
            progress.setVisibility(View.GONE);
            mImageView.setVisibility(View.VISIBLE);
        }
    }
}
