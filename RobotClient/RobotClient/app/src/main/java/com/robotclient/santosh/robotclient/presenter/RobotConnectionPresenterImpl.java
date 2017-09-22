package com.robotclient.santosh.robotclient.presenter;

import android.util.Log;

import com.robotclient.santosh.robotclient.MainActivity;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

/**
 * Created by santosh on 13-09-2017.
 */

public class RobotConnectionPresenterImpl implements RobotConnectionPresenter{
    private final static String HOST_NAME = "10.9.45.11"; /*"10.9.45.43"*/;
    private final static int PORT_NUMBER =/* 9999;*/ 9999;
    private static final String TAG = RobotConnectionPresenterImpl.class.getName();
    private ThreadExecutor threadExecutor;
    private Socket hostSocket;
    private PrintWriter out;
    private BufferedReader in;

    public RobotConnectionPresenterImpl()   {
        threadExecutor= new ThreadExecutor();
        new Thread(new Runnable() {
            @Override
            public void run() {
                openConnection();
            }
        }).start();
    }

    /**
     * It opens connection with Pepper robot.
     */
    @Override
    public void openConnection() {
        try {
            hostSocket = new Socket(HOST_NAME, PORT_NUMBER);
            out = new PrintWriter(hostSocket.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(hostSocket.getInputStream()));
        } catch (UnknownHostException e) {
            System.err.println("Don't know about host " + HOST_NAME);
            System.exit(1);
        } catch (IOException e) {
            System.err.println("Couldn't get I/O for the connection to " + HOST_NAME);
            System.exit(1);
        }
    }

    /**
     * It create job to write data to opened connection with Pepper.
     * @param command
     */

    @Override
    public void writeToConnection(String command) {
        threadExecutor.execute(command);
    }

    /**
     * It write data to opened connection with Pepper.
     * @param command
     */
    private synchronized void writeCommand(String command) {
        if (command != null) {
            out.println(command);
        }
        Log.v(TAG,"Command is sent to Server Socket" + command);
    }

    /**
     * ThreadPool to assign created job to threads.
     */
    public class ThreadExecutor {
        private final int CORE_POOL_SIZE = Runtime.getRuntime().availableProcessors();
        private final int MAX_POOL_SIZE = CORE_POOL_SIZE;
        private final int KEEP_ALIVE_TIME = 120;
        private final TimeUnit TIME_UNIT = TimeUnit.SECONDS;
        private final BlockingQueue<Runnable> WORK_QUEUE = new LinkedBlockingQueue<Runnable>();
        private ThreadPoolExecutor mThreadPoolExecutor;

        ThreadExecutor() {
            long keepAlive = KEEP_ALIVE_TIME;
            mThreadPoolExecutor = new ThreadPoolExecutor(
                    CORE_POOL_SIZE,
                    MAX_POOL_SIZE,
                    keepAlive,
                    TIME_UNIT,
                    WORK_QUEUE);

        }

        /**
         * Execute command to write it to Socket.
         * @param command
         */
        public void execute(final String command) {
            mThreadPoolExecutor.submit(new Runnable() {
                @Override
                public void run() {
                    writeCommand(command);
                }
            });
        }
    }
}
