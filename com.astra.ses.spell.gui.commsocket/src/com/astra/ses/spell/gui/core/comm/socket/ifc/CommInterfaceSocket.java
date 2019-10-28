///////////////////////////////////////////////////////////////////////////////
//
// PACKAGE   : com.astra.ses.spell.gui.core.comm.socket.ifc
// 
// FILE      : CommInterfaceSocket.java
//
// DATE      : 2008-11-24 08:34
//
// Copyright (C) 2008, 2015 SES ENGINEERING, Luxembourg S.A.R.L.
//
// By using this software in any way, you are agreeing to be bound by
// the terms of this license.
//
// All rights reserved. This program and the accompanying materials
// are made available under the terms of the Eclipse Public License v1.0
// which accompanies this distribution, and is available at
// http://www.eclipse.org/legal/epl-v10.html
//
// NO WARRANTY
// EXCEPT AS EXPRESSLY SET FORTH IN THIS AGREEMENT, THE PROGRAM IS PROVIDED
// ON AN "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, EITHER
// EXPRESS OR IMPLIED INCLUDING, WITHOUT LIMITATION, ANY WARRANTIES OR
// CONDITIONS OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY OR FITNESS FOR A
// PARTICULAR PURPOSE. Each Recipient is solely responsible for determining
// the appropriateness of using and distributing the Program and assumes all
// risks associated with its exercise of rights under this Agreement ,
// including but not limited to the risks and costs of program errors,
// compliance with applicable laws, damage to or loss of data, programs or
// equipment, and unavailability or interruption of operations.
//
// DISCLAIMER OF LIABILITY
// EXCEPT AS EXPRESSLY SET FORTH IN THIS AGREEMENT, NEITHER RECIPIENT NOR ANY
// CONTRIBUTORS SHALL HAVE ANY LIABILITY FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING WITHOUT LIMITATION
// LOST PROFITS), HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OR DISTRIBUTION OF THE PROGRAM OR THE
// EXERCISE OF ANY RIGHTS GRANTED HEREUNDER, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGES.
//
// Contributors:
//    SES ENGINEERING - initial API and implementation and/or initial documentation
//
// PROJECT   : SPELL
//
// SUBPROJECT: SPELL GUI Client
//
///////////////////////////////////////////////////////////////////////////////
package com.astra.ses.spell.gui.core.comm.socket.ifc;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketAddress;
import java.net.UnknownHostException;
import java.util.concurrent.atomic.AtomicLong;

import org.eclipse.jface.dialogs.MessageDialog;
import org.eclipse.jface.dialogs.TitleAreaDialog;
import org.eclipse.jface.window.Window;
import org.eclipse.swt.SWT;
import org.eclipse.swt.events.ModifyEvent;
import org.eclipse.swt.events.ModifyListener;
import org.eclipse.swt.graphics.Point;
import org.eclipse.swt.graphics.Rectangle;
import org.eclipse.swt.layout.GridData;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.Control;
import org.eclipse.swt.widgets.Display;
import org.eclipse.swt.widgets.Label;
import org.eclipse.swt.widgets.Shell;
import org.eclipse.swt.widgets.Text;

import com.astra.ses.spell.gui.core.comm.messages.SPELLmessage;
import com.astra.ses.spell.gui.core.comm.messages.SPELLmessageEOC;
import com.astra.ses.spell.gui.core.comm.messages.SPELLmessageError;
import com.astra.ses.spell.gui.core.comm.socket.processing.IncomingMessage;
import com.astra.ses.spell.gui.core.comm.socket.processing.IncomingRequest;
import com.astra.ses.spell.gui.core.comm.socket.processing.InputReader;
import com.astra.ses.spell.gui.core.comm.socket.processing.OutputWriter;
import com.astra.ses.spell.gui.core.comm.socket.utils.FileTransfer;
import com.astra.ses.spell.gui.core.comm.socket.utils.Mailbox;
import com.astra.ses.spell.gui.core.comm.socket.utils.Tunneler;
import com.astra.ses.spell.gui.core.exceptions.CommException;
import com.astra.ses.spell.gui.core.interfaces.ICommInterface;
import com.astra.ses.spell.gui.core.interfaces.ICommListener;
import com.astra.ses.spell.gui.core.model.notification.ErrorData;
import com.astra.ses.spell.gui.core.model.server.AuthenticationData;
import com.astra.ses.spell.gui.core.model.server.ServerInfo;
import com.astra.ses.spell.gui.core.model.types.Level;
import com.astra.ses.spell.gui.core.utils.Logger;
import com.trilead.ssh2.Session;

/*******************************************************************************
 * @brief Communication interface socket-based implementation.
 * @date 22/04/08
 ******************************************************************************/
public class CommInterfaceSocket implements ICommInterface
{
	/** Holds the server details */
	private ServerInfo m_serverInfo;
	/** Registration key */
	private String m_key;
	/** Holds the comm socket */
	private Socket m_socket;
	/** Listener for receiving messages and requests */
	private ICommListener m_listener;
	/** Incoming messages processor */
	private InputReader m_reader;
	/** Outgoing messages processor */
	private OutputWriter m_writer;
	/** Configured timeout */
	private long m_responseTimeout;
	/** Tunneler */
	private Tunneler m_tunneler;
	/** SCP client */
	private FileTransfer m_scp;
	/** Message mailbox for response distribution */
	private Mailbox m_responseMailbox;
	/** Sequence counter */
	private AtomicLong m_seqCount;
	/** Holds the local host name */
	private String m_localHostname;
	private String m_localFullyQualifiedName;
	private String m_localIpAddress;
	
	public class LoginDialog extends TitleAreaDialog{

		// Widgets
		private Text textUsername;
		private Text textPassword;
		private String localPassword;
		private String localUsername;

		public LoginDialog(Shell parent) {
			super(parent);
		}
		
		public String getUsername(){
			return localUsername;
		}
		
		public String getPassword(){
			return localPassword;
		}
		
		@Override
		protected Control createContents(Composite parent) {
			Control contents = super.createContents(parent);
			setTitle("Credentials for Restarting SPELL Listener");
			setMessage("Please provide the credentials to login for restarting the listener.");
			return contents;
		}
		
		@Override
		protected Control createDialogArea(Composite parent) {

			Composite area = (Composite) super.createDialogArea(parent);

			Composite container = new Composite(area, SWT.NULL);
			container.setLayout(new GridLayout(2, false));
			container.setLayoutData(new GridData(GridData.FILL_BOTH));
			
			new Label(container, SWT.NULL).setText("Username");
			textUsername = new Text(container, SWT.BORDER);
			textUsername.setLayoutData(new GridData(GridData.FILL_HORIZONTAL));
			textUsername.setText(localUsername);
			textUsername.addModifyListener(new ModifyListener() {
				
				@Override
				public void modifyText(ModifyEvent e) {
					
					localUsername = ((Text) e.widget).getText();
					
				}
			});
			new Label(container, SWT.NULL).setText("Password");
			textPassword = new Text(container, SWT.PASSWORD | SWT.BORDER);
			textPassword.setLayoutData(new GridData(GridData.FILL_HORIZONTAL));
			textPassword.setText(localPassword);
			textPassword.addModifyListener(new ModifyListener() {
				
				@Override
				public void modifyText(ModifyEvent e) {
					
					localPassword = ((Text) e.widget).getText();
					
				}
			});
			return area;
		}

		public void setPassword(String password) {
			localPassword = password;
		}

		public void setUsername(String username) {
			localUsername = username;
		}
	}

	/***************************************************************************
	 * Constructor
	 **************************************************************************/
	public CommInterfaceSocket()
	{
		m_socket = null;
		m_seqCount = new AtomicLong(0);
		m_serverInfo = null;
		m_reader = null;
		m_writer = null;
		m_responseTimeout = 5000;
		m_key = null;
		m_tunneler = null;
		m_scp = null;
		m_responseMailbox = new Mailbox();
		try
		{
	        m_localHostname = java.net.InetAddress.getLocalHost().getHostName();
        }
        catch (UnknownHostException e)
        {
	        m_localHostname = null;
        }
		try
        {
	        m_localIpAddress = java.net.InetAddress.getLocalHost().getHostAddress();
        }
        catch (UnknownHostException e)
        {
	        m_localIpAddress = null;
        }
		try
        {
	        m_localFullyQualifiedName = java.net.InetAddress.getLocalHost().getCanonicalHostName();
        }
        catch (UnknownHostException e)
        {
	        m_localFullyQualifiedName = null;
        }
	}

	/***************************************************************************
	 * Configure the interface to connect to the given server and port
	 * 
	 * @param server
	 *            SPELL server hostname
	 * @param port
	 *            SPELL server port
	 **************************************************************************/
	public void configure(ServerInfo info)
	{
		m_serverInfo = info;
	}

	/***************************************************************************
	 * 
	 **************************************************************************/
	private boolean isLocalServer()
	{ 
		if (m_localHostname != null)
		{
			if (m_serverInfo.getHost().equals(m_localHostname)) return true;
		}
		if (m_localFullyQualifiedName != null)
		{
			if (m_serverInfo.getHost().equals(m_localFullyQualifiedName)) return true;
		}
		if (m_localIpAddress != null)
		{
			if (m_serverInfo.getHost().equals(m_localIpAddress)) return true;
		}
		if (m_serverInfo.getHost().equals("localhost")) return true;
		if (m_serverInfo.getHost().equals("127.0.0.1")) return true;

		try
		{
			String serverFullyQualifiedName =
				InetAddress.getByName(m_serverInfo.getHost()).getCanonicalHostName();
			
			if (serverFullyQualifiedName.equals(m_localFullyQualifiedName))
			{
				return true;
			}
		}
		catch (UnknownHostException e)
		{
			// do nothing
		}
		return false; 
	}

	/***************************************************************************
	 * Returns whether the local filesystem is forced to be used as file
	 * transfer mechanism.
	 **************************************************************************/
	private boolean hasLocalAccess()
	{ 
		AuthenticationData authentication = m_serverInfo.getAuthentication(); 
		return authentication != null && authentication.isLocalAccess(); 
	}

	public String shorten(String msg){
		String[] split = msg.split("\n");
		StringBuilder result = new StringBuilder();
		if (split.length > 10){
			for(int idx = 0;idx < 5;idx++){
				result.append(split[idx]);
				result.append("\n");
			}
			result.append("...\n");
			for(int idx = split.length - 5;idx < split.length;idx++){
				result.append(split[idx]);
				result.append("\n");
			}
			return result.toString();
		} else {
			return msg;
		}
		
	}
	
	@Override
	public synchronized void restart() throws CommException {
		if (m_listener == null)
		{
			throw new CommException("No listener available, cannot connect");
		}
		try
		{
			Logger.info("Connecting IPC interface to " + m_serverInfo.getName(), Level.PROC, this);
			// Enable tunneling if needed
			boolean tunneling = false;
			if (m_serverInfo.getAuthentication() != null)
			{
				if (hasLocalAccess())
				{
					Logger.info("No need for SSH tunneling - local access being used", Level.PROC, this);
				}
				else if (m_serverInfo.getAuthentication().isClearMode())
				{
					Logger.info("No need for SSH tunneling - clear mode configured", Level.PROC, this);
				}
				else
				{
					
					final AuthenticationData login = AuthenticationData.valueOf(m_serverInfo.getAuthentication().toString());
					Display.getDefault().syncExec(new Runnable() {
						
						@Override
						public void run() {
							Shell shell = new Shell(Display.getDefault().getActiveShell());
							LoginDialog dialog = new LoginDialog(shell);
							dialog.setPassword(login.getPassword());
							dialog.setUsername(login.getUsername());
							if (shell.getParent() != null) {
		                        Rectangle parentSize = shell.getParent().getBounds();
		                        Rectangle shellSize = shell.getBounds();
		                        int locationX = (parentSize.width - shellSize.width) / 2 + parentSize.x;
		                        int locationY = (parentSize.height - shellSize.height) / 2 + parentSize.y;
		                        shell.setLocation(new Point(locationX, locationY));
		                    }
							if (dialog.open() == Window.OK) {
								login.setUsername(dialog.getUsername());
								login.setPassword(dialog.getPassword());
							}
							shell.dispose();
						}
					});
					AuthenticationData oldLogin = m_serverInfo.getAuthentication();
					m_serverInfo.setAuthentication(login);
					Logger.info("Enabling SSH tunneling to " + m_serverInfo.getName(), Level.PROC, this);
					setTunneling(m_serverInfo);
					m_tunneler.openTunnel();
					tunneling = true;
					m_serverInfo.setAuthentication(oldLogin);
				}
			}
			
			if (m_serverInfo.getHost() == null)
			{
				Logger.debug("Cannot restart no host given!", Level.COMM, this);
				
			}
			else
			{
				if (!m_serverInfo.getSatellite().isEmpty()){
					Session session = m_tunneler.getConnection().openSession();
					try{
						session.requestPTY("xterm");
						session.startShell();
						OutputStream stdin = session.getStdin();
						InputStream stdout = session.getStdout();
						InputStream stderr = session.getStderr();
						stdin.write(("/bin/bash\nif [ -z \"${SPELL_HOME}\" ]; then\ncd /home/spell/SPELL/bin/\nelse\ncd $SPELL_HOME/bin/\nfi\n./SPELL-Server " + m_serverInfo.getSatellite() + " &\ndisown\nsleep 5 && echo SPELL Restart finished.\n").getBytes());
						
						Integer exitStatus = session.getExitStatus();
						StringBuilder errorResult = new StringBuilder();
						StringBuilder fullResult = new StringBuilder();
						long start = System.currentTimeMillis();
						while (true){
							exitStatus = session.getExitStatus();
							String result = readAllFromStream(stdout);
							String err = readAllFromStream(stderr);
							errorResult.append(err);
							fullResult.append(result);
							fullResult.append(err);
							if ((result.contains("SPELL Restart finished.") || err.contains("SPELL Restart finished.")) && !result.contains("echo ")){
								break;
							}
							if (System.currentTimeMillis() - start > 20000){
								throw new CommException("\nCould not restart Listener within 20s!\nSPELL Listener output:\n" + shorten(fullResult.toString()));
							}
						}
						
						Logger.debug("SPELL Listener restart report:\n" + fullResult.toString(), Level.COMM, this);
						
						//MessageDialog.openInformation(Display.getDefault().getActiveShell(), "SPELL Listener Restart Log", "Logged messages:\n" + shorten(fullResult.toString()) + "\n\nClick on OK to continue.");
					} finally {
						if (tunneling)
							m_tunneler.closeTunnel();
						session.close();
					}
				}
				
				
			}
			
		}
		catch (Exception ex)
		{
			throw new CommException(ex);
		}
	}

	private String readAllFromStream(InputStream stdout) throws IOException {
		byte[] buf = new byte[stdout.available()];
		int length = stdout.read(buf);
		String result = new String(buf,0,length);
		return result;
	}
	
	/***************************************************************************
	 * Connect to the SPELL server
	 **************************************************************************/
	public synchronized void connect() throws CommException
	{
		if (m_listener == null)
		{
			throw new CommException("No listener available, cannot connect");
		}
		try
		{
			Logger.info("Connecting IPC interface to " + m_serverInfo.getName(), Level.PROC, this);
			// Enable tunneling if needed
			boolean tunneling = false;
			if (m_serverInfo.getAuthentication() != null)
			{
				if (hasLocalAccess())
				{
					Logger.info("No need for SSH tunneling - local access being used", Level.PROC, this);
				}
				else if (m_serverInfo.getAuthentication().isClearMode())
				{
					Logger.info("No need for SSH tunneling - clear mode configured", Level.PROC, this);
				}
				else
				{
					Logger.info("Enabling SSH tunneling to " + m_serverInfo.getName(), Level.PROC, this);
					setTunneling(m_serverInfo);
					m_tunneler.openTunnel();
					tunneling = true;
				}
			}
			
			if (m_serverInfo.getHost() == null)
			{
				Logger.debug("Connecting as server to port " + m_serverInfo.getPort(), Level.COMM, this);
				ServerSocket srv = new ServerSocket(m_serverInfo.getPort());
				m_socket = srv.accept();
			}
			else
			{
				m_socket = new Socket();
				m_socket.setKeepAlive(true);
				m_socket.setSoTimeout(0);
				m_socket.setSoLinger(false, 0);
				SocketAddress addr = null;
				if (tunneling)
				{
					Logger.debug("Tunneling to server at " + m_serverInfo.getHost() + ":" + m_serverInfo.getPort(), Level.PROC, this);
					addr = new InetSocketAddress(InetAddress.getByName("localhost"), m_tunneler.getLocalPort());
				}
				else
				{
					Logger.debug("Connecting to server at " + m_serverInfo.getHost() + ":" + m_serverInfo.getPort(), Level.PROC, this);
					addr = new InetSocketAddress(InetAddress.getByName(m_serverInfo.getHost()), m_serverInfo.getPort());
				}
				m_socket.connect(addr);
			}
			Logger.debug("Connected", Level.COMM, this);
			
			if (isLocalServer() || hasLocalAccess())
			{
				Logger.info("Using local file transfers", Level.COMM, this);
				m_scp = new FileTransfer();
			}
			else
			{
				Logger.info("Using remote file transfers", Level.COMM, this);
				
				if (m_serverInfo.getAuthentication()==null)
				{
					Logger.warning("Warning: no authentication methods available to perform file transfers!", Level.COMM, this);
					m_scp = null;
				}
				else // Have authentication
				{
					// If we are tunneling, profit from the tunnel connection
					if (tunneling)
					{
						m_scp = new FileTransfer( m_tunneler.getConnection(), m_serverInfo );
					}
					// otherwise create a new SCP connection
					else
					{
						m_scp = new FileTransfer( null, m_serverInfo );
					}
					Logger.debug("File transfers prepared", Level.COMM, this);
				}
			}
			
			DataInputStream in = new DataInputStream(m_socket.getInputStream());
			DataOutputStream out = new DataOutputStream(m_socket.getOutputStream());

			Logger.debug("Reading key information", Level.COMM, this);
			writeMyKey(out);
			readMyKey(in);

			m_reader = new InputReader(this, in);
			m_reader.start();
			m_writer = new OutputWriter(out, m_key);

			Logger.debug("Ready", Level.COMM, this);
		}
		catch (Exception ex)
		{
			m_socket = null;
			throw new CommException(ex.getLocalizedMessage(),ex);
		}
	}

	/***************************************************************************
	 * Disconnect from SPELL server sending EOC
	 **************************************************************************/
	public synchronized void disconnect() throws CommException
	{
		doDisconnect(false);
		if (m_listener != null)
		{
			m_listener.connectionClosed();
		}
	}

	/***************************************************************************
	 * Disconnect from SPELL server abruptly
	 **************************************************************************/
	public synchronized void forceDisconnect() throws CommException
	{
		doDisconnect(true);
	}

	/***************************************************************************
	 * Check if the interface is connected
	 * 
	 * @return True if it is connected
	 **************************************************************************/
	public boolean isConnected()
	{
		if (m_socket == null)
			return false;
		boolean socketOpen = !m_socket.isClosed();
		boolean ioOk = (!m_socket.isInputShutdown() && !m_socket.isOutputShutdown());
		return (socketOpen && ioOk);
	}

	/***************************************************************************
	 * Send a message to the SPELL server
	 * 
	 * @param msg
	 *            SPELL message
	 **************************************************************************/
	public synchronized void sendMessage(SPELLmessage msg) throws CommException
	{
		m_writer.send(msg);
	}

	/***************************************************************************
	 * Send a request to the SPELL server with custom timeout
	 * 
	 * @param msg
	 *            SPELL request
	 * @return SPELL response message
	 **************************************************************************/
	public SPELLmessage sendRequest(SPELLmessage msg, long timeout) throws CommException
	{
		SPELLmessage response = null;
		msg.setSequence(m_seqCount.getAndIncrement());
		String msgId = msg.getReceiver() + "-" + msg.getSender() + ":" + msg.getSequence();
		try
		{
			m_responseMailbox.prepare(msgId);
			m_writer.send(msg);
			response = m_responseMailbox.retrieve(msgId, timeout);
		}
		catch (Exception ex)
		{
			ex.printStackTrace();
		}
		return response;
	}

	/***************************************************************************
	 * Send a request to the SPELL server with default timeout
	 * 
	 * @param msg
	 *            SPELL request
	 * @return SPELL response message
	 **************************************************************************/
	public SPELLmessage sendRequest(SPELLmessage msg) throws CommException
	{
		return sendRequest(msg, m_responseTimeout);
	}

	/***************************************************************************
	 * Download a file from peer
	 **************************************************************************/
	public void getFile( String remoteFile, String targetDir ) throws CommException
	{
		try
		{
			if (m_scp == null)
			{
				throw new CommException("Unable download file '" + remoteFile + "':\n\nNo authentication parameters in configuration");
			}
			m_scp.getFile(remoteFile, targetDir);
		}
		catch(IOException ex)
		{
			throw new CommException("Failed to download file '" + remoteFile + "':\n\n " + ex.getLocalizedMessage());
		}
	}

	/***************************************************************************
	 * Assign the message listener
	 * 
	 * @param listener
	 *            The target for incoming messages and requests
	 **************************************************************************/
	public void setCommListener(ICommListener listener)
	{
		m_listener = listener;
	}

	/***************************************************************************
	 * Obtain the interface key
	 **************************************************************************/
	public String getKey()
	{
		return m_key;
	}

	/***************************************************************************
	 * Enable tunneling
	 **************************************************************************/
	public void setTunneling(ServerInfo info)
	{
		Logger.info("Enabled SSH tunneling", Level.COMM, this);
		m_tunneler = new Tunneler(info);
	}

	/***************************************************************************
	 * Response timeout
	 **************************************************************************/
	public void setResponseTimeout(long timeoutUSecs)
	{
		m_responseTimeout = timeoutUSecs;
	}

	/***************************************************************************
	 * InputData reader places responses here
	 **************************************************************************/
	public void incomingResponse(String id, SPELLmessage msg)
	{
		if ((msg instanceof SPELLmessageError))
		{
			if (m_responseMailbox.isWaitingFor(id))
			{
				m_responseMailbox.place(id, msg);
			}
			else
			{
				new IncomingMessage(id, msg, m_listener).enqueue();
			}
		}
		else
		{
			m_responseMailbox.place(id, msg);
		}
	}

	/***************************************************************************
	 * InputData reader places requests here
	 **************************************************************************/
	public void incomingRequest(String id, SPELLmessage msg)
	{
		new IncomingRequest(id, msg, m_listener, m_writer).enqueue();
	}

	/***************************************************************************
	 * InputData reader places messages here
	 **************************************************************************/
	public void incomingMessage(String id, SPELLmessage msg)
	{
		new IncomingMessage(id, msg, m_listener).enqueue();
	}

	/***************************************************************************
	 * Report a communication failure
	 * 
	 * @param msg
	 **************************************************************************/
	public void commFailure(String msg, String reason)
	{
		if (!isConnected())
			return;
		Logger.error("Communication layer failure: " + msg + ", " + reason, Level.COMM, this);
		forceDisconnect();
		if (m_listener != null)
		{
			ErrorData data = new ErrorData(null, msg, reason, true);
			m_listener.connectionLost(data);
		}
	}

	// =========================================================================
	// # NON-ACCESSIBLE METHODS
	// =========================================================================

	/***************************************************************************
	 * Read the client key
	 **************************************************************************/
	private void readMyKey(DataInputStream in) throws CommException
	{
		try
		{
			int counter = 0;
			while (in.available() == 0)
			{
				Thread.sleep(10);
				counter += 10;
				if (counter > 1000)
				{
					throw new CommException("Server is not responding");
				}
			}
			Logger.debug("Waiting registration key", Level.COMM, this);
			byte keyb1 = in.readByte();
			byte keyb2 = in.readByte();
			int key = keyb1;
			int key2 = key << 8;
			key2 += keyb2;
			m_key = Integer.toString(key2);
			Logger.debug("Registered with key: " + m_key, Level.COMM, this);
		}
		catch (Exception ex)
		{
			throw new CommException(ex.getLocalizedMessage());
		}
	}

	/***************************************************************************
	 * Write the client key (0 to request one)
	 **************************************************************************/
	private void writeMyKey(DataOutputStream out) throws CommException
	{
		try
		{
			out.writeByte(0);
			out.writeByte(0);
		}
		catch (Exception ex)
		{
			throw new CommException(ex.getLocalizedMessage());
		}
	}

	/***************************************************************************
	 * Disconnect from SPELL server
	 **************************************************************************/
	private void doDisconnect(boolean force) throws CommException
	{
		if (!isConnected())
			return;
		try
		{
			Logger.debug("Disconnecting", Level.COMM, this);
			if (!force)
			{
				Logger.debug("Sending EOC", Level.COMM, this);
				SPELLmessage msg = new SPELLmessageEOC();
				sendMessage(msg);
			}
			m_socket.shutdownInput();
			m_socket.shutdownOutput();
			m_socket.close();
			Logger.debug("Disconnected", Level.COMM, this);
			if (m_reader != null)
			{
				m_reader.setWorking(false);
				m_reader.interrupt();
				m_reader = null;
			}
			m_writer = null;
			m_socket = null;
			if (m_tunneler != null)
			{
				m_tunneler.closeTunnel();
				m_tunneler = null;
			}
			if (m_scp != null && m_tunneler == null)
			{
				m_scp.close();
			}
		}
		catch (Exception ex)
		{
			throw new CommException("Error in disconnection (force=" + force + "): " + ex.getLocalizedMessage());
		}
	}

}
