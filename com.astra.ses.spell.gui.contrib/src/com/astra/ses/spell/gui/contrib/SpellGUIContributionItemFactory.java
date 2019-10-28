package com.astra.ses.spell.gui.contrib;

public class SpellGUIContributionItemFactory {
	
	public static SpellGUIContributionItem createContribution(String type){
		if (type.toUpperCase().startsWith("DISPLAY")){
			return new SpellGUIDisplayContributionItem();
		}
		return null;
		
	}
	
}
