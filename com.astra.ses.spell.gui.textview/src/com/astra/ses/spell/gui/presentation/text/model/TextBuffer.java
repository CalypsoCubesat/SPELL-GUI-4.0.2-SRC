///////////////////////////////////////////////////////////////////////////////
//
// PACKAGE   : com.astra.ses.spell.gui.presentation.text.model
// 
// FILE      : TextBuffer.java
//
// DATE      : 2008-11-21 13:54
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
package com.astra.ses.spell.gui.presentation.text.model;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FilenameFilter;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.RandomAccessFile;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.WeakHashMap;

/******************************************************************************
 * Holds a buffer of strings that can be inspectioned through a data window of
 * smaller dimensions. Whenever a line is added to the buffer, the window
 * scrolls up a line as well so that the impression of scrolling is created. The
 * window position and size can be changed by means of the
 * <code>setWindowPosition</code> method. The size of the buffer grows
 * automatically by chunks of size <code>m_scalationRatio</code> with a default
 * value of 50.
 * 
 *****************************************************************************/
public class TextBuffer
{
	/** The default amount of lines that the buffer will use to grow */
	public static final int DEFAULT_SCALATION_RATIO = 50;
	/** The maximum amount of lines allowed for the buffer */
	private int m_capacity;
	/** Holds the list of registered listeners */
	private ArrayList<TextBufferListener> m_listeners;
	/** Holds the buffer data */
	private TextViewLine[] m_buffer = new TextViewLine[0];
	/** Holds the amount of lines stored */
	private int m_lineCount;
	/** Holds the currently programmed scalation ratio */
	private int m_scalationRatio;
	/** Start position of the view window */
	private int m_bufferStart = -1;
	private int m_bufferLength = -1;
	private int m_windowStart;
	/** Length of the view window */
	private int m_windowLength;
	/** True if the data window must scroll following the new data */
	private boolean m_scrollWindow;

	private HashMap<Integer,Long> indexCache = new HashMap<Integer,Long>();
	private RandomAccessFile bufferFile;
	private MappedByteBuffer textViewFileBuffer;
	private File tempBufferfile;
	private FileChannel fileChannel;
	private int currentOffset = 0;
	private static final int CACHE_SIZE = 1024 * 1024 * 10;
	
	private WeakHashMap<Integer, TextViewLine> cachedLines = new WeakHashMap<Integer, TextViewLine>();	
	
	public void initBuffer(){
		try {
			tempBufferfile = File.createTempFile("spell-proc-text-buffer", "");
			File[] files = tempBufferfile.getParentFile().listFiles(new FilenameFilter() {
				
				@Override
				public boolean accept(File dir, String name) {
					// TODO Auto-generated method stub
					return name.contains("spell-proc-text-buffer");
				}
			});
			for (File file : files) {
				if (!file.equals(tempBufferfile)){
					try {
						file.delete();
					} catch (Exception ex){
						
					}
				}
			}
			bufferFile = new RandomAccessFile(tempBufferfile, "rw");

	        fileChannel = bufferFile.getChannel();
	        
			textViewFileBuffer = fileChannel.map(FileChannel.MapMode.READ_WRITE, 0, CACHE_SIZE);
			currentOffset = 0;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        
	}
	
	public synchronized void cacheLine(TextViewLine line){
		try{
			long currentPos = textViewFileBuffer.position() + currentOffset;
			byte[] serializeLine = serializeObject(line);
			int currentLength = serializeLine.length;
			if (currentPos + currentLength + 4 - currentOffset > textViewFileBuffer.capacity()*0.8){
				try {
					textViewFileBuffer.force();
					textViewFileBuffer = fileChannel.map(FileChannel.MapMode.READ_WRITE, currentPos, CACHE_SIZE);
					currentOffset = (int)currentPos;
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
			//System.out.println(currentLength);
			textViewFileBuffer.putInt(currentLength);
			textViewFileBuffer.put(serializeLine);

			indexCache.put(m_lineCount, currentPos);
			
		} catch (Exception ex){
			ex.printStackTrace();
		}
		
	}
	
	public synchronized TextViewLine getCachedLine(int lineNumber){
		TextViewLine textViewLine = cachedLines.get(lineNumber);
		if (textViewLine != null)
			return textViewLine;
		
		int oldPos = textViewFileBuffer.position();
		try {
			Long currentPos = indexCache.get(lineNumber);
			if (currentPos == null)
				return null;
			if (currentPos.intValue() - currentOffset > 0){
				textViewFileBuffer.position(currentPos.intValue() - currentOffset);
				int size = textViewFileBuffer.getInt();
				byte[] buf = new byte[size];
				textViewFileBuffer.get(buf);
				TextViewLine line = deserializeObject(buf);
				cachedLines.put(lineNumber, line);
				return line;
			} else {
				try {
					bufferFile.seek(currentPos);
					int size = bufferFile.readInt();
					byte[] buf = new byte[size];
					bufferFile.read(buf, 0, size);
					TextViewLine line = deserializeObject(buf);
					cachedLines.put(lineNumber, line);
					return line;
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
					return getCachedLine(lineNumber);
				}
			}
		} catch (java.nio.BufferUnderflowException ex){
			ex.printStackTrace();
			return  getCachedLine(lineNumber);
		} finally {
			textViewFileBuffer.position(oldPos);
		}
		
	}
	
	
	public static byte[] serializeObject(TextViewLine line) {
		try {
			ByteArrayOutputStream bytesOut = new ByteArrayOutputStream();
			ObjectOutputStream oos = new ObjectOutputStream(bytesOut);
		    oos.writeObject(line);
		    oos.flush();
		    byte[] bytes = bytesOut.toByteArray();
		    bytesOut.close();
		    oos.close();
		    return bytes;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return null;
	}
	public TextViewLine deserializeObject(byte[] data) {
		TextViewLine line = null;
	    try {
	        ByteArrayInputStream bytesIn = new ByteArrayInputStream(data);
	        ObjectInputStream ois = new ObjectInputStream(bytesIn);
	        line = (TextViewLine) ois.readObject();
	        ois.close();
	    } catch (ClassNotFoundException e) {
	        e.printStackTrace();
	    } catch (IOException e) {
			e.printStackTrace();
		}
	    return line;
	}
	
	/**************************************************************************
	 * Constructor.
	 *************************************************************************/
	public TextBuffer( int capacity )
	{

		m_listeners = new ArrayList<TextBufferListener>();
		m_scalationRatio = DEFAULT_SCALATION_RATIO;
		setBuffer(new TextViewLine[0]);
		m_lineCount = 0;
		m_windowStart = 0;
		m_windowLength = DEFAULT_SCALATION_RATIO;
		m_scrollWindow = false;
		m_capacity = capacity;
		initBuffer();
	}

	/**************************************************************************
	 * Register a buffer change listener
	 *************************************************************************/
	public void addBufferListener(TextBufferListener lst)
	{
		m_listeners.add(lst);
	}

	/**************************************************************************
	 * De-register a buffer change listener
	 *************************************************************************/
	public void removeBufferListener(TextBufferListener lst)
	{
		m_listeners.remove(lst);
	}

	/**************************************************************************
	 * Toggle timestamp
	 *************************************************************************/
	public void setShowTimestamp(boolean show)
	{
		if (getBuffer() != null)
			for (TextViewLine line : getBuffer())
			{
				if (line != null)
					line.setShowTimestamp(show);
			}
	}

	/**************************************************************************
	 * Se buffer capacity
	 *************************************************************************/
	public void setCapacity( int lines )
	{
		m_capacity = lines;
		if (m_capacity==-1) return;
		if (m_capacity <= m_lineCount)
		{
			//regenerate();
		}
	}

	/**************************************************************************
	 * Regenerate buffer when growing beyond capacity
	 *************************************************************************/
	private void regenerate()
	{
		if (m_capacity < m_scalationRatio)
		{
			setBuffer(new TextViewLine[ m_scalationRatio ]);
			m_lineCount = 0;
			System.gc();
		}
		else if (m_lineCount > m_scalationRatio)
		{
			// These are the lines we are going to keep: last scalation ratio + extra lines
			int numBlocks = (m_lineCount / m_scalationRatio);
			if (numBlocks > 0)
				numBlocks -= 1;
			int toRemove = m_scalationRatio * numBlocks;
			int newLineCount = m_lineCount - toRemove;
			
			TextViewLine[] newData = new TextViewLine[ m_scalationRatio ];
			System.arraycopy(getBuffer(), toRemove, newData, 0, newLineCount);
			setBuffer(newData);
			newData = null;
			m_lineCount = newLineCount;
			System.gc();
			m_windowStart = 0;
			m_windowLength = DEFAULT_SCALATION_RATIO;
		}
	}

	/**************************************************************************
	 * Append a line to the buffer (synchornized)
	 *************************************************************************/
	private synchronized void processNewLine( TextViewLine line )
	{
		cacheLine(line);
		// If the buffer is full, enlarge it or dump initial lines if too big
//		if (m_capacity != -1 && m_lineCount == m_capacity)
//		{
//			regenerate();
//		}
//		else if (m_lineCount == m_buffer.length) // The buffer is full
//		{
//			TextViewLine[] newData = new TextViewLine[m_buffer.length + m_scalationRatio];
//			System.arraycopy(m_buffer, 0, newData, 0, m_buffer.length);
//			m_buffer = newData;
//			newData = null;
//			System.gc();
//		}
//
//		// If there are no lines, just add it
//		if (m_lineCount == 0)
//		{
//			m_buffer[0] = line;
//		}
//		else
//		// Remaining space in buffer, add the line
//		{
//			TextViewLine previousLine = m_buffer[m_lineCount - 1];
//			// If requires ordering
//			if (line.compareTo(previousLine) < 0)
//			{
//				int index = Arrays.binarySearch(m_buffer, 0, m_lineCount - 1, line);
//				if (index < 0) // We need to insert
//				{
//					// (-insertion_point -1)
//					index = -index - 1;
//				}
//				// If the index is at the end, just insert
//				if (index == m_lineCount)
//				{
//					m_buffer[m_lineCount] = line;
//				}
//				else
//				{
//					// Now insert the data
//					TextViewLine[] newData = new TextViewLine[m_buffer.length + 1];
//					System.arraycopy(m_buffer, 0, newData, 0, index);
//					newData[index] = line;
//					System.arraycopy(m_buffer, index, newData, index + 1, m_lineCount - index + 1);
//					m_buffer = newData;
//					newData = null;
//					System.gc();
//				}
//			}
//			else
//			// If not, add the line at the end
//			{
//				m_buffer[m_lineCount] = line;
//			}
//		}

		m_lineCount++;
	}
	
	/**************************************************************************
	 * Append a line to the buffer
	 *************************************************************************/
	public void append(TextViewLine line)
	{
		processNewLine(line);

		if ((m_lineCount > (m_windowStart + m_windowLength)) && m_scrollWindow)
		{
			// Shift the window to simulate the scrolling effect
			m_windowStart++;
			// Notify that the window has moved
			fireWindowMoved();
		}
		else
		{
			// Notify that the data has changed
			fireDataChanged();
		}
	}

	/**************************************************************************
	 * Clear the buffer
	 *************************************************************************/
	public void clear()
	{
		setBuffer(new TextViewLine[m_scalationRatio]);
		m_lineCount = 0;
		fireDataCleared();
		
	}
	@Override
	protected void finalize() throws Throwable {
		bufferFile.close();
		tempBufferfile.deleteOnExit();
		super.finalize();
	}
	/**************************************************************************
	 * Set the scalation ratio
	 *************************************************************************/
	public void setScalationRatio(int ratio)
	{
		m_scalationRatio = ratio;
	}

	/**************************************************************************
	 * Change the view window position and length
	 *************************************************************************/
	public void setWindowPosition(int start, int length, boolean autoscroll)
	{
		m_windowStart = start;
		m_windowLength = length;
		m_scrollWindow = autoscroll;
		fireWindowMoved();
	}

	/**************************************************************************
	 * Set the data stored in the buffer
	 *************************************************************************/
//	public void setData(TextViewLine[] lines)
//	{
//		setBuffer(new TextViewLine[lines.length]);
//		m_lineCount = lines.length;
//		System.arraycopy(lines, 0, getBuffer(), 0, lines.length);
//	}

	/**************************************************************************
	 * Get the amount of data stored in the buffer
	 *************************************************************************/
	public synchronized int getDataSize()
	{
		return m_lineCount;
	}

	/**************************************************************************
	 * Get the all data stored
	 *************************************************************************/
	public synchronized TextViewLine[] getData()
	{
		TextViewLine[] data = new TextViewLine[m_lineCount];
		for (int i = 0; i < data.length; i++) {
			data[i] = getCachedLine(i);
		}
		return data;
	}

	/**************************************************************************
	 * Get the data window position
	 *************************************************************************/
	public synchronized int getDataWindowStart()
	{
		return m_windowStart;
	}

	/**************************************************************************
	 * Get the data window size
	 *************************************************************************/
	public synchronized int getDataWindowLength()
	{
		return m_windowLength;
	}

	/**************************************************************************
	 * Get the data covered by the view window
	 *************************************************************************/
	public synchronized TextViewLine[] getWindowData()
	{
//		// Try to get a full data window
//		int lengthToCopy = m_windowLength;
//		// If the window ends after the max number of lines
//		if ((m_windowStart + m_windowLength) > m_lineCount)
//		{
//			// If the window even starts after the max number of lines
//			if (m_windowStart > m_lineCount)
//			{
//				// We return nothing
//				return new TextViewLine[0];
//			}
//			// We return a non-full window data
//			lengthToCopy = m_lineCount - m_windowStart;
//		}
//		// Create a buffer for the copied data and copy it
//		TextViewLine[] data = new TextViewLine[lengthToCopy];
//		System.arraycopy(getBuffer(), m_windowStart, data, 0, lengthToCopy);
		return getBuffer();
	}

	/**************************************************************************
	 * Fire a data changed event
	 *************************************************************************/
	private void fireDataChanged()
	{
		for (TextBufferListener lst : m_listeners)
		{
			lst.dataChanged(this);
		}
	}

	/**************************************************************************
	 * Fire a data cleared event
	 *************************************************************************/
	private void fireDataCleared()
	{
		for (TextBufferListener lst : m_listeners)
		{
			lst.dataCleared(this);
		}
	}

	/**************************************************************************
	 * Fire a data window moved event
	 *************************************************************************/
	private void fireWindowMoved()
	{
		for (TextBufferListener lst : m_listeners)
		{
			lst.dataWindowMoved(this);
		}
	}

	private TextViewLine[] getBuffer() {
		boolean showTimeStamp = true;
		if (m_buffer.length > 0){
			showTimeStamp = m_buffer[0].isShowTimestamp();
		}
		if (m_windowStart != m_bufferStart){
			int bufferStart = m_windowStart;
			ArrayList<TextViewLine> buffer = new ArrayList<TextViewLine>();
			for (int i = 0; i < m_windowLength; i++) {
				int requestedLine = bufferStart + i;
				TextViewLine cachedLine = getCachedLine(requestedLine);
				if (cachedLine == null)
					break;
				
				cachedLine.setShowTimestamp(showTimeStamp);
				buffer.add(cachedLine);
			}
			m_buffer = buffer.toArray(new TextViewLine[buffer.size()]);
			m_bufferStart = bufferStart;
			m_bufferLength = m_buffer.length;
		} else if (m_windowLength != m_bufferLength){
			ArrayList<TextViewLine> buffer = new ArrayList<TextViewLine>();
			for (TextViewLine textViewLine : m_buffer) {
				buffer.add(textViewLine);
			}
			for (int i = m_bufferLength; i < m_windowLength; i++) {
				int requestedLine = m_windowStart + i;
				TextViewLine cachedLine = getCachedLine(requestedLine);
				if (cachedLine == null)
					break;
				cachedLine.setShowTimestamp(showTimeStamp);
				buffer.add(cachedLine);
			}
			m_buffer = buffer.toArray(new TextViewLine[buffer.size()]);
			m_bufferStart = m_windowStart;
			m_bufferLength = m_buffer.length;
		}
		return m_buffer;
	}

	private void setBuffer(TextViewLine[] m_buffer) {
		//this.m_buffer = m_buffer;
	}
}
