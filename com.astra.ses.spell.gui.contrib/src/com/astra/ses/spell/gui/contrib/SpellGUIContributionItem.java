package com.astra.ses.spell.gui.contrib;

import java.util.HashMap;
import java.util.List;

import org.eclipse.swt.graphics.Color;
import org.eclipse.swt.graphics.Font;
import org.eclipse.swt.widgets.Composite;

import com.astra.ses.spell.gui.core.interfaces.ServiceManager;
import com.astra.ses.spell.gui.core.model.types.ItemStatus;
import com.astra.ses.spell.gui.preferences.interfaces.IConfigurationManager;
import com.astra.ses.spell.gui.preferences.keys.FontKey;

public abstract class SpellGUIContributionItem {
	protected static IConfigurationManager  s_cfg = null;

	protected static Color s_okColor = null;
	protected static Color s_warnColor = null;
	protected static Color s_errorColor = null;
	protected static HashMap<String,Color> colorMap = new HashMap<String,Color>();
	protected static Font s_boldFont = null;
	
	protected static Color getColor(List<String> data){
		Color c = colorMap.get(data.get(data.size()-1).toUpperCase());
		if (c == null)
			c = s_warnColor;
		return c;
	}
	
	public SpellGUIContributionItem() {
		if (s_okColor == null)
		{
			s_cfg = (IConfigurationManager) ServiceManager.get(IConfigurationManager.class);
			//s_proxy = (IContextProxy) ServiceManager.get(IContextProxy.class);
			s_okColor = s_cfg.getStatusColor(ItemStatus.SUCCESS);
			s_warnColor = s_cfg.getStatusColor(ItemStatus.WARNING);
			s_errorColor = s_cfg.getStatusColor(ItemStatus.ERROR);
			s_boldFont = s_cfg.getFont(FontKey.GUI_BOLD);
			colorMap.put("RED", s_errorColor);
			colorMap.put("YELLOW", s_warnColor);
			colorMap.put("", s_warnColor);
			colorMap.put("GREEN", s_okColor);
		}
	}
	
	public abstract void setData(List<String> data);
	
	public abstract void createContent(Composite parent);
	
	public abstract Composite getRoot();
	
	public abstract void update();
	
	public abstract void dispose();
}
	