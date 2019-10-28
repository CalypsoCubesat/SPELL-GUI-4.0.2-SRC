package com.astra.ses.spell.gui.contrib;

import java.util.Collections;
import java.util.List;

import org.eclipse.swt.SWT;
import org.eclipse.swt.graphics.Color;
import org.eclipse.swt.layout.GridData;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.Label;

public class SpellGUIDisplayContributionItem extends SpellGUIContributionItem {

	private List<String> data = Collections.EMPTY_LIST;
	private Composite root = null;
	private Label valueLabel;
	private Label keyLabel;
	
	@Override
	public void setData(List<String> data) {
		this.data  = data;
	}

	@Override
	public void createContent(Composite parent) {
		root = new Composite(parent, SWT.NONE);

		GridLayout layout = new GridLayout();
		layout.marginHeight = 0;
		layout.marginWidth = 0;
		layout.horizontalSpacing = 5;
		layout.marginLeft = 0;
		layout.marginRight = 0;
		layout.numColumns = 2;
		root.setLayout(layout);
		
		GridData serverLabelData = new GridData(SWT.CENTER, SWT.CENTER, false, true);
		keyLabel = new Label(root, SWT.NONE);
		keyLabel.setText(data.get(0) + ":");
		keyLabel.setFont(s_boldFont);
		keyLabel.setLayoutData(serverLabelData);
		
		// WIDGET
		GridData serverWidgetData = new GridData(SWT.CENTER, SWT.CENTER, false, true);
		valueLabel = new Label(root, SWT.BORDER);
		valueLabel.setText(" "+ data.get(1) + " ");
		valueLabel.setBackground(getColor(data));
		valueLabel.setAlignment(SWT.CENTER);
		valueLabel.setLayoutData(serverWidgetData);
		
		root.computeSize(SWT.DEFAULT, SWT.DEFAULT);
		root.update();
		root.pack();
	}

	@Override
	public Composite getRoot() {
		// TODO Auto-generated method stub
		return root;
	}

	@Override
	public void update() {
		keyLabel.setText(data.get(0) + ":");
		valueLabel.setText(" "+ data.get(1) + " ");
		valueLabel.setBackground(getColor(data));
		keyLabel.pack();
		valueLabel.pack();
		root.pack();
	}

	@Override
	public void dispose() {
		root.dispose();
	}

}
