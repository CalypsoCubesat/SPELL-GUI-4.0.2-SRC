///////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2013 GMV S.A.U.
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
///////////////////////////////////////////////////////////////////////////////
package com.astra.ses.spell.gui.clock;

import java.text.DateFormat;
import java.util.Date;

import org.eclipse.jface.action.ControlContribution;
import org.eclipse.jface.action.ToolBarManager;
import org.eclipse.swt.SWT;
import org.eclipse.swt.graphics.Point;
import org.eclipse.swt.graphics.Rectangle;
import org.eclipse.swt.layout.GridData;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.Control;
import org.eclipse.swt.widgets.Display;
import org.eclipse.swt.widgets.Label;
import org.eclipse.swt.widgets.ToolBar;
import org.eclipse.ui.PlatformUI;
import org.eclipse.ui.internal.WorkbenchWindow;
import org.eclipse.ui.menus.WorkbenchWindowControlContribution;

import com.astra.ses.spell.gui.core.interfaces.ServiceManager;
import com.astra.ses.spell.gui.preferences.interfaces.IConfigurationManager;

/**
 * This class provides a clock control that can be put in a toolbar.
 */
public class ClockControlContribution extends WorkbenchWindowControlContribution
{
	/**
	 * This class provides a thread that updates the clock time.
	 */
	private class ClockThread extends Thread
	{
		/** The period between clock refreshes */
		private static final int REFRESH_MS = 500;

		/** The thread runs while this variable is true */
		public volatile boolean m_keepRunning = true;
		
		/* (non-Javadoc)
		 * @see java.lang.Thread#run()
		 */
		@Override
		public void run()
		{
			while (m_keepRunning)
			{
				final Date date = m_clockService.getTime();
				PlatformUI.getWorkbench().getDisplay().syncExec(new Runnable() {
					@Override
					public void run()
					{
				        setTime(date);
					}
				});
				
				try
				{
					Thread.sleep(REFRESH_MS);
				}
				catch (InterruptedException e)
				{
					// Ok, probably someone asked the thread to stop
				}
			}
		}
		
		/** Stop the thread when possible */
		public void finish()
		{
			m_keepRunning = false;
			interrupt();
		}
	}
	
	/** The application configuration */
	private static IConfigurationManager s_cfg =
		(IConfigurationManager) ServiceManager.get(IConfigurationManager.class);
	private static DateFormat s_dateFormat = s_cfg.getTimeFormat(); 
	
	/** The label showing the date */
	private Label m_clockLabel;
	
	/** The thread updating the date */
	private ClockThread m_clockThread;
	
	/** The service that provides the time */
	private ClockService m_clockService;
	
	
	/* (non-Javadoc)
	 * @see org.eclipse.jface.action.ControlContribution#createControl(org.eclipse.swt.widgets.Composite)
	 */
	@Override
	protected Control createControl(Composite parent)
	{

        m_clockService = new ClockService();
        m_clockService.start();
        
		Composite base = new Composite(parent, SWT.NULL); 

        GridLayout layout = new GridLayout();
        layout.marginTop = 0;
        layout.marginHeight = 0;
        layout.marginWidth = 0;
        layout.marginLeft = 5;
        layout.marginRight = 0;
        layout.marginBottom = 0;
        layout.numColumns = 1;
        base.setLayout( layout );
        
        m_clockLabel = new Label(base, SWT.BORDER);
        m_clockLabel.setBackground(Display.getCurrent().getSystemColor(SWT.COLOR_WHITE));
        m_clockLabel.setAlignment(SWT.CENTER);
        setTime(m_clockService.getTime());

        m_clockThread = new ClockThread();
        m_clockThread.start();
        Point computeSize = base.computeSize(SWT.DEFAULT, SWT.DEFAULT);
        return base;
	}
	
	/* (non-Javadoc)
	 * @see org.eclipse.jface.action.ContributionItem#dispose()
	 */
	@Override
	public void dispose()
	{
		m_clockThread.finish();
		m_clockService.finish();
		super.dispose();
	}	
	
	/**
	 * Sets the time shown in the control
	 */
	private void setTime(Date d)
	{
		if (!m_clockLabel.isDisposed())
		{
			m_clockLabel.setText(s_dateFormat.format(d));
			m_clockLabel.setToolTipText("Clock is " + m_clockService.getClockOffset()/1000 + " seconds off compared to the GCS.");
			if (getParent() != null)
			getParent().update(true);
			update();
		}
	}
	@Override
	public boolean isDirty() {
		// TODO Auto-generated method stub
		return true;
	}
	@Override
	public boolean isDynamic() {
		return true;
	}
	
	
}
