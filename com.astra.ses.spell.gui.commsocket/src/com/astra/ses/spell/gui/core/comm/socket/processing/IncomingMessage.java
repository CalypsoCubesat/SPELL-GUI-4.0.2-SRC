///////////////////////////////////////////////////////////////////////////////
//
// PACKAGE   : com.astra.ses.spell.gui.core.comm.socket.processing
// 
// FILE      : IncomingMessage.java
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
package com.astra.ses.spell.gui.core.comm.socket.processing;

import java.util.Hashtable;
import java.util.PriorityQueue;
import java.util.concurrent.ConcurrentLinkedQueue;

import com.astra.ses.spell.gui.core.comm.messages.SPELLmessage;
import com.astra.ses.spell.gui.core.interfaces.ICommListener;
import com.astra.ses.spell.gui.core.model.types.Level;
import com.astra.ses.spell.gui.core.utils.Logger;

public class IncomingMessage implements Comparable<IncomingMessage>
{
	protected static final int MAX_NUMBER_WORKERS = 5;
	protected static final Hashtable<String,ConcurrentLinkedQueue<IncomingMessage>> queuedRequests = new Hashtable<String,ConcurrentLinkedQueue<IncomingMessage>>();

	protected String name;
	private ICommListener	m_listener;
	private SPELLmessage	m_message;

	public static void dispose(String key) {
		queuedRequests.remove(key);
	}
	
	public IncomingMessage(String id, SPELLmessage msg, ICommListener listener)
	{
		super();
		name = "i-msg-" + id;
		m_message = msg;
		m_listener = listener;
	}

	public void enqueue(){
		//System.err.println(m_message.getSequence() + " - received for " + m_message.getSender());
		final String currentSender = m_message.getSender();
		ConcurrentLinkedQueue<IncomingMessage> queue = queuedRequests.get(currentSender);
		if (queue == null) {
			final ConcurrentLinkedQueue<IncomingMessage> finalQueue = new ConcurrentLinkedQueue<IncomingMessage>();
			queue = finalQueue;
			queuedRequests.put(currentSender, finalQueue);
			new Thread("Incoming Message Worker for " + currentSender){
				private PriorityQueue<IncomingMessage> messageBuffer = new PriorityQueue<IncomingMessage>();
				private long currentSequence = -1;
				private long lastUpdate = -1;
				@Override
				public void run() {
					while (queuedRequests.getOrDefault(currentSender, null) == finalQueue || !finalQueue.isEmpty()){
						try{
							IncomingMessage poll = finalQueue.poll();
							if (poll != null){
								SPELLmessage msg = poll.m_message;
								if (currentSequence == -1)
									currentSequence = msg.getSequence();
								if (msg.getSequence() <= currentSequence) {
									poll.dispatch();
									lastUpdate = System.currentTimeMillis();
									if (currentSequence >= 0)
										currentSequence++;
								} else {
									messageBuffer.add(poll);
									//System.err.println(messageBuffer);
									IncomingMessage current = messageBuffer.peek();
									while(current != null && current.getSequence() == currentSequence) {
										current = messageBuffer.poll();
										current.dispatch();
										//System.err.println("Delayed dispatch - " + current.getSequence());
										lastUpdate = System.currentTimeMillis();
										currentSequence++;
										current = messageBuffer.peek();
									}
								}
							} else {
								if (!messageBuffer.isEmpty() && System.currentTimeMillis() - lastUpdate > 50) {
									//System.err.println(currentSender  + " missed message " + currentSequence);
									IncomingMessage poll2 = messageBuffer.poll();
									currentSequence = poll2.getSequence();
									//System.err.println("Delayed dispatch - " + poll2.getSequence());
									poll2.dispatch();
									currentSequence++;
								} else {
									Thread.sleep(50);
								}
							}
						} catch (Exception ex) {
							ex.printStackTrace();
							Logger.error(ex.getLocalizedMessage(), Level.COMM, this);
						}
					}
					Logger.info("Dispatching for " + currentSender + " closed.", Level.COMM, this);
				};
			}.start();
		}
			
		queue.add(this);
		if (queue.size() % 5000 == 4999) {
			System.err.println("Too many packets are arriving("+queue.size()+")!");
		}
	}
	
	public void dispatch()
	{
		m_listener.receiveMessage(m_message);
	}

	public long getSequence() {
		return m_message.getSequence();
	}
	
	@Override
	public int compareTo(IncomingMessage arg0) {
		return this.m_message.compareTo(arg0.m_message);
	}
	
	@Override
	public String toString() {
		return "["+getSequence()+"]" + name + " " + m_message.getId();
	}
}
