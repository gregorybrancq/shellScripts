// @ExecutionModes({on_single_node="main_menu_scripting/freeplaneGTD[addons.listNextActions]"})
//========================================================= 
//	Freeplane GTD
//
//	Groovy script to extract GTD-style Next Action list
//	from a Freeplane mind map
//
//	Version 0.8
//	
//	Copyright (c)2011 Auxilus Systems LLC
//
// 	This program is free software: you can redistribute it and/or modify
//	it under the terms of the GNU General Public License as published by
//	the Free Software Foundation, either version 3 of the License, or
//	any later version.
//
//	This program is distributed in the hope that it will be useful,
//	but WITHOUT ANY WARRANTY; without even the implied warranty of
//	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//	GNU General Public License for more details.
//
//	You should have received a copy of the GNU General Public License
//	along with this program.  If not, see <http://www.gnu.org/licenses/>.
// 
//=========================================================


//=========================================================
//	references
//=========================================================
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import javax.swing.text.*;
import javax.swing.text.html.HTMLEditorKit;
import javax.swing.text.html.StyleSheet;
import javax.swing.ImageIcon;
import javax.swing.UIManager;

import java.awt.*;
import java.awt.BorderLayout;
import java.awt.datatransfer.*;
import java.awt.Dimension;
import java.awt.event.*;
import java.awt.event.KeyEvent;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.GridLayout;
import java.awt.print.*;
import java.awt.Toolkit;

import java.net.URL;

import java.text.ParsePosition;
import java.text.SimpleDateFormat;

import java.util.Date;

import org.freeplane.core.ui.components.UITools;
import org.freeplane.plugin.script.proxy.ControllerProxy;
import org.freeplane.plugin.script.proxy.Proxy;
import org.freeplane.core.resources.ResourceController;


//=========================================================
//	classes
//=========================================================

//---------------------------------------------------------
// GTDReport: creates GUI for next action lists
//---------------------------------------------------------
public class GTDReport {
	
	private static GTDReport gtdReport = new GTDReport();
	
	private String txtVer = "0.8";
	private GTDMapReader gtdMapReader;
	private Proxy.Controller ctrl;	
	private String ByProject = "";
	private String ByWhere = "";
	private String ByWho = "";
	private String ByWhen = "";
	private int selTab = 0;
	private String userPath = "";
	private JLabel reportByProject = new JLabel();
	private JLabel reportByWhere = new JLabel();
	private JLabel reportByWho = new JLabel();
	private JLabel reportByWhen = new JLabel();
	private JEditorPane htmlByProject = new JEditorPane("text/html", "Project");
	private JEditorPane htmlByWhere = new JEditorPane("text/html", "Where");
	private JEditorPane htmlByWho = new JEditorPane("text/html", "Who");
	private JEditorPane htmlByWhen = new JEditorPane("text/html", "When");
	private JTabbedPane tabbedPane = new JTabbedPane();
	
	//--------------------------------------------------------------
	// private constructor for singleton pattern
	private GTDReport() {
						 		
	}
	
	public static synchronized GTDReport getInstance(){
		return gtdReport;
	}
	 
	protected JComponent makeTextPanel(JEditorPane filler) {
		JPanel panel = new JPanel(false);		
		filler.setEditable(false);
		filler.addHyperlinkListener(new NodeLink(this));
		HTMLEditorKit kit = (HTMLEditorKit)filler.getEditorKit();
		StyleSheet styleSheet = kit.getStyleSheet();
		styleSheet.addRule("body {color:#000000; font-family:Verdana, Arial; font-size:12pt; padding: 10px 25px 0px 25px; }");
		styleSheet.addRule("h1 {font-size:20pt; font-weight:bold}");		
		styleSheet.addRule("a {text-decoration: none; color:#990000;}");
		panel.setLayout(new GridLayout(1, 1));
		panel.add(filler);
		return panel;
	}
	
	private JPanel buildReportPanel(){
		
		// setup panel to contain tabbed pane
		JPanel reportPanel = new JPanel();
		reportPanel.setLayout(new GridLayout(1,1));	
		ImageIcon icon = null;	
		
		// build By Project tab
		JComponent panel1 = makeTextPanel(htmlByProject);
		panel1.setBackground(Color.WHITE);
		JScrollPane scrollpane1 = new JScrollPane(panel1);
		tabbedPane.addTab("<html><body height=50><b><i>By Project</i></b><br/><h1 style='color:#666666; font-size:24pt; text-align:center;'>" + gtdMapReader.getCountNextActions().toString() + "</h1></body></html>", icon, scrollpane1, "List next actions by project");
		
		// build By Who tab
		JComponent panel3 = makeTextPanel(htmlByWho);
		panel3.setBackground(Color.WHITE);
		JScrollPane scrollpane3 = new JScrollPane(panel3);
		tabbedPane.addTab("<html><body height=50><b><i>By Who</i></b><br/><h1 style='color:#666666; font-size:24pt; text-align:center;'>" + gtdMapReader.getCountDelegated().toString() + "</h1></body></html>", icon, scrollpane3, "List next actions by owners (who)");
		
		// build By Where tab 
		JComponent panel2 = makeTextPanel(htmlByWhere);
		panel2.setBackground(Color.WHITE);
		JScrollPane scrollpane2 = new JScrollPane(panel2);
		tabbedPane.addTab("<html><body height=50><b><i>By Where</i></b></body></html>", icon, scrollpane2, "List next actions by context (where done)");		
		
		// build By When tab 
		JComponent panel4 = makeTextPanel(htmlByWhen);
		panel4.setBackground(Color.WHITE);
		JScrollPane scrollpane4 = new JScrollPane(panel4);
		tabbedPane.addTab("<html><body height=50><b><i>By When</i></b></body></html>", icon, scrollpane4, "List next actions by due date (when)");		
		
		// build About tab
		String txtAbout = "<html><body style='padding-left:25px;'><h1>Freeplane|<span style='color:#ff3300;'>GTD</span></h1><h2>Version " + txtVer + "</h2></body></html>";
		JPanel panel5 = new JPanel(false);		
		String imgURL = userPath + "/resources/images/fpgtdLogo.png";
		//UITools.informationMessage(imgURL.toString());
		ImageIcon iconLogo = null;
		if (imgURL!=null){
			iconLogo = new ImageIcon(imgURL);
		}
		JLabel appName = new JLabel(txtAbout,iconLogo,JLabel.CENTER);
		appName.setHorizontalAlignment(JLabel.CENTER);
		panel5.setLayout(new GridLayout(2, 1));
		panel5.add(appName);
		JLabel linkURL = new JLabel("<html><h4>Auxilus Systems LLC<br/>Licensed under GNU GPL Version 3</h4><a href='http://ordino.auxilus.com/freeplanegtd'>http://ordino.auxilus.com/freeplanegtd</a></html>");
		linkURL.setHorizontalAlignment(JLabel.CENTER);
		linkURL.setCursor(new Cursor(Cursor.HAND_CURSOR));
		linkURL.addMouseListener(new MouseAdapter() {
			public void mouseClicked(MouseEvent e) {
				URI uriLink = new URI("http://ordino.auxilus.com/freeplanegtd");
				browseLink(uriLink);
			}
		});
		panel5.add(linkURL);
		panel5.setBackground(Color.WHITE);
		JScrollPane scrollpane5 = new JScrollPane(panel5);
		tabbedPane.addTab("<html><body height=50><b><i>About</i></b></body></html>", icon, scrollpane5, "About Freeplane|GTD");
		
		// Enable scrolling tabs and set location
		tabbedPane.setTabLayoutPolicy(JTabbedPane.SCROLL_TAB_LAYOUT);
		tabbedPane.setTabPlacement(JTabbedPane.RIGHT);
		
		// Register a change listener to track selected tab
		tabbedPane.addChangeListener(new ChangeListener() {
			public void stateChanged(ChangeEvent evt) {
				JTabbedPane pane = (JTabbedPane)evt.getSource();

				// Get current tab index
				selTab = pane.getSelectedIndex();
			}
		});
		
		// Add the tabbed pane to this panel.
		reportPanel.add(tabbedPane);
		
		return reportPanel;
	}
	
	public String ProjectReport() {
		return ByProject;
	}
	
	public String ContextReport() {
		return ByWhere;
	}
	
	public String OwnerReport() {
		return ByWho;
	}
	
	public String DueReport() {
		return ByWhen;
	}
	
	public int TabIndex(){
		return selTab;
	}
	
	public void setUserPath(String path){
		userPath = path;
	}
	
	public void setController(Proxy.Controller controller){
		ctrl = controller;
	}
	
	public Proxy.Controller getController(){
		return ctrl;
	}
	
	public void setMapReader(GTDMapReader MapReader){
		gtdMapReader = MapReader;
		this.Refresh();	
	}
	
	private static void browseLink(URI uri) {
		if (Desktop.isDesktopSupported()) {
		  try {
			Desktop.getDesktop().browse(uri);
		  } catch (IOException e) { /* TODO: error handling */ }
		} else { /* TODO: error handling */ }
	}
		
	public void Show() {		
		//Create and set up the window
		ImageIcon icon = new ImageIcon(userPath + "/icons/fpgtdIcon.png");
		JFrame frame = new JFrame("Freeplane|GTD Next Actions");
		frame.setIconImage(icon.getImage());
		frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
		 
		//Add next action report panel to the window
		JPanel reportPanel = this.buildReportPanel();
		frame.add(reportPanel, BorderLayout.CENTER);
		
		// Add command buttons
		JPanel cmdPanel = new JPanel();
		BoxLayout boxH = new BoxLayout(cmdPanel, BoxLayout.X_AXIS);
		cmdPanel.setLayout(boxH);
		JButton refreshButton = new JButton("Refresh");
		refreshButton.addActionListener(new RefreshUIWindow(this));
		JButton printButton = new JButton("Print");
       	printButton.addActionListener(new PrintUIWindow(this));
		JButton copyButton = new JButton("Copy");
		copyButton.addActionListener(new CopyUIWindow(this));		
		JButton cancelButton = new JButton("Cancel");
		cancelButton.addActionListener(new CloseUIWindow(frame));
		cmdPanel.add(refreshButton);
		cmdPanel.add(printButton);
		cmdPanel.add(copyButton);
		cmdPanel.add(cancelButton);		
		frame.add(cmdPanel, BorderLayout.SOUTH);
       		
		// make the frame half the height and width
  		Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
  		int frHeight = (screenSize.height)/2;
  		int frWidth = (screenSize.width)/2;
		
		//Display the window
		frame.pack();
		frame.setSize(frWidth,frHeight);		
		frame.setLocationRelativeTo(UITools.frame);
		frame.setVisible(true);
	}
	
	public void Refresh() {
		// Get next actions from GTD mind map
		gtdMapReader.ParseMap();
		
		// Get HTML for next action lists
		ByProject = gtdMapReader.getHTMLByProject();
		ByWhere = gtdMapReader.getHTMLByWhere();
		ByWho = gtdMapReader.getHTMLByWho();
		ByWhen = gtdMapReader.getHTMLByWhen();
		
		// add reports to labels
		htmlByProject.setText(ByProject);
		htmlByWhere.setText(ByWhere);
		htmlByWho.setText(ByWho);
		htmlByWhen.setText(ByWhen);
		
		// update counts on tabs
		if (tabbedPane.tabCount>0){
			tabbedPane.setTitleAt(0, "<html><body height=50>By Project<br/><h1 style='color:#666666;text-align:center;'>" + gtdMapReader.getCountNextActions().toString() + "</h1></body></html>");
			tabbedPane.setTitleAt(1, "<html><body height=50>By Who<br/><h1 style='color:#666666;text-align:center;'>" + gtdMapReader.getCountDelegated().toString() + "</h1></body></html>");
		}
	}

}


//---------------------------------------------------------
// GTDMapReader: reads and parses GTD map for next actions
//---------------------------------------------------------
public class GTDMapReader {
	
	private String ByProject = "";
	private String ByWhere = "";
	private String ByWho = "";
	private String ByWhen = "";
	private int CountNextActions = 0;
	private int CountDelegated = 0;
	private String htmlBodyStyle = "<html><body>\n";
	private String IconNextAction = "yes";
	private String IconProject = "list";
	private String IconToday = "excellent";
	private String NodeNextActionIcon ="Icon: Next action";
	private String NodeProjectIcon ="Icon: Project";
	private String NodeTodayIcon ="Icon: Today";
	private Proxy.Node RootNode;
	private def NAList;
	private def ProjectList;
	
	//--------------------------------------------------------------
	// constructor
	public GTDMapReader(Proxy.Node rootNode){
		
		RootNode = rootNode;
		
	}
	
	//--------------------------------------------------------------
	// properties
	public String getNextActionIcon() {		
		IconNextAction = findIconKey(RootNode,NodeNextActionIcon,IconNextAction);
		return IconNextAction;		
	}
	
	public String getProjectIcon() {		
		IconProject = findIconKey(RootNode,NodeProjectIcon,IconProject);
		return IconProject;		
	}
	
	public String getTodayIcon(){
		IconToday = findIconKey(RootNode,NodeTodayIcon,IconToday);
		return IconToday;
	}
	
	public def getProjectList(){		
		ProjectList = findProjects(RootNode,IconProject);
		return ProjectList;
	}
	
	public def getNAList(){
		NAList = findNextActions(RootNode, ProjectList,IconNextAction,IconToday);
		return NAList;
	}
	
	public int getCountNextActions(){
		return CountNextActions;
	}
	
	public int getCountDelegated(){
		return CountDelegated;
	}
	
	public String getHTMLByProject(){
		ByProject = htmlBodyStyle;
		def naByProject = NAList.groupBy{it['project']};
		naByProject = naByProject.sort{it.toString().toLowerCase()};
		if(naByProject.size()>0) {
			CountNextActions = 0;
			naByProject.each {
				key, value -> String strProject = key;
				ByProject += "<h1>" + strProject + "</h1>\n<ul>\n";
				naByProject[strProject].each {
					CountNextActions = CountNextActions + 1;
					String strWhere = it['where'];
					String strWho = it['who'];
					String strWhen = it['when'];
					if (strWho=="tbd"){strWho = "";}
					if (strWhen=="tbd"){strWhen = "";}
					String strOwner = "";
					String strDue = "";
					if (strWho.length()>0){strOwner = "[" + strWho + "]";}
					if (strWhen.length()>0){strDue = "{" + strWhen + "}";}
					String strAssign = strOwner + " " + strDue;
					strAssign = strAssign.trim();
					ByProject += "\t<li><a href='" + it['nodeID'] + "'>" + it['action'] + "</a>" + " @" + strWhere + " " + strAssign + "</li>\n";
				}
				ByProject += "</ul>\n";
			}
		}
		else {
			ByProject += "<h1 style='color:#666666;'>No Next Actions Found On This Map</h1><p>Make sure to mark Next Actions with icon specified by 'Icon:Next action' node under 'Settings' node</p>"
		}
		
		ByProject += "</body></html>";
		
		return ByProject;
	}
	
	public String getHTMLByWhere(){
		ByWhere = htmlBodyStyle;
		def naByWhere = NAList.groupBy{it['where']};
		naByWhere = naByWhere.sort{it.toString().toLowerCase()};
		if (naByWhere.size()>0){
			naByWhere.each {
				key, value -> String strWhere = key;
				ByWhere += "<h1>" + strWhere + "</h1>\n<ul>\n";
				naByWhere[strWhere].each {
					String strProject = it['project'];
					String strWho = it['who'];
					String strWhen = it['when'];
					if (strWho=="tbd"){strWho = "";}
					if (strWhen=="tbd"){strWhen = "";}
					String strOwner = "";
					String strDue = "";
					if (strWho.length()>0){strOwner = "[" + strWho + "]";}
					if (strWhen.length()>0){strDue = "{" + strWhen + "}";}
					String strAssign = strOwner + " " + strDue;
					strAssign = strAssign.trim();					
					ByWhere += "\t<li><a href='" + it['nodeID'] + "'>" + it['action'] + "</a>" + " (for: " + strProject + ")" + " " + strAssign + "</li>\n";
				}
				ByWhere += "</ul>\n";
			}
		}
		else {
			ByWhere += "<h1 style='color:#666666;'>No Next Actions Found On This Map</h1><p>Make sure to mark Next Actions with icon specified by 'Icon:Next action' node under 'Settings' node</p>"
		}
		ByWhere += "</body></html>";
		
		return ByWhere;
	}
	
	public String getHTMLByWho(){
		ByWho = htmlBodyStyle;
		def naByWho = NAList.groupBy{it['who']};
		naByWho = naByWho.sort{it.toString().toLowerCase()};
		CountDelegated = 0;
		naByWho.each {
			key, value -> String strWho = key;
			if (strWho!="tbd"){
				ByWho += "<h1>" + strWho + "</h1>\n<ul>\n";
				naByWho[strWho].each {
					CountDelegated = CountDelegated + 1;
					String strProject = it['project'];
					String strWhen = it['when'];
					if (strWhen=="tbd"){strWhen = "";}
					strWhen = strWhen.trim();
					if (strWhen.length()>0){strWhen = " {" + strWhen + "}";}
					ByWho += "\t<li><a href='" + it['nodeID'] + "'>" + it['action'] + "</a>" + " (for: " + strProject + ")" + strWhen + "</li>\n";
				}
				ByWho += "</ul>\n";
			}
		}
		if (ByWho == htmlBodyStyle){		
			ByWho += "<h1 style='color:#666666;'>No Delegated Next Actions Found On This Map</h1><p>Use ALT-F9 to add a 'Who' attribute to a Next Action node</p>";
		}
		ByWho += "</body></html>";
		
		return ByWho;
	}
	
	public String getHTMLByWhen(){
		ByWhen = htmlBodyStyle;
		def naByWhen = NAList.groupBy{it['when']};
		naByWhen = naByWhen.sort{it.toString().toLowerCase()};
		naByWhen = sortDateWhen(naByWhen);		
		naByWhen.each {
			key, value -> String strWhen = key;
			if (strWhen!="tbd"){
				ByWhen += "<h1>" + strWhen + "</h1>\n<ul>\n";
				naByWhen[strWhen].each {
					String strProject = it['project'];
					String strWho = it['who'];
					if (strWho=="tbd"){strWho = "";}
					strWho = strWho.trim();
					if (strWho.length()>0){strWho = " [" + strWho + "]";}
					ByWhen += "\t<li><a href='" + it['nodeID'] + "'>" + it['action'] + "</a>" + " (for: " + strProject + ")" + strWho + "</li>\n";
				}
				ByWhen += "</ul>\n";
			}
		}
		if (ByWhen == htmlBodyStyle) {
			ByWhen += "<h1 style='color:#666666;'>No Due Dates for Next Actions Found On This Map</h1><p>Use ALT-F9 to add a 'When' attribute to a Next Action node</p>";
		}

		ByWhen += "</body></html>";
		
		return ByWhen;
	}
	
	private def sortDateWhen(def naByWhen){
		def newByWhen = [:];
		
		// Today goes first, followed by This Week
		if(naByWhen.containsKey('Today')){newByWhen['Today'] = naByWhen['Today'];}
		if(naByWhen.containsKey('This Week')){newByWhen['This Week'] = naByWhen['This Week'];}
		
		// Now add any other dates
		naByWhen.each {
			key, value -> String strWhen = key;
			if(strWhen!="Today" && strWhen!="This Week"){				
				newByWhen[strWhen] = naByWhen[strWhen];
			}	
		}
		
		return newByWhen;
	}
	
	//--------------------------------------------------------------
	//Get icon key names from Settings/Icons nodes
	private String findIconKey(Proxy.Node thisNode, String nodeLabel, String iconLast){		
		def icons = thisNode.icons.icons;
		String nodeText = thisNode.text;
		String iconFound = iconLast;
				
		if (nodeText.trim() == nodeLabel){
			iconFound = icons[0];
		}
			
		thisNode.children.each {
						
			iconFound = findIconKey(it, nodeLabel, iconFound);
				
		}
		return iconFound;	
	}
	
	//--------------------------------------------------------------
	// recursive walk through nodes to find Projects
	private def findProjects(Proxy.Node thisNode, String iconProject){
		def icon = thisNode.icons.icons;
		def result = [];
			
		// include result if it has project icon and its not the icon setting node for projects
		if (icon[0] == iconProject){
			if (!(thisNode.text =~ /Icon:/)){
				result = [thisNode];
			}
		}
			
		thisNode.children.each {
								
			result += findProjects(it, iconProject);
		}
					
		return result;		
	}
	
	//--------------------------------------------------------------
	// find parent for the next action, either direct (task) or indirect (project)
	private def findNextActionProject(Proxy.Node thisNode, listProjects){		
		Proxy.Node parentNode = thisNode.getParent();
		def naProject = parentNode.text;
			
		listProjects.each {
			if (it!=null && thisNode.isDescendantOf(it)){
				naProject = it.text;
			}
		}
			
		return naProject;		
	}
	
	//--------------------------------------------------------------
	// recursive walk through nodes to find Next Actions
	private def findNextActions(Proxy.Node thisNode, listProjects, String iconNextAction, String iconToday){				
		def icons = thisNode.icons.icons;
		def naAction = thisNode.text;
		def naNodeID = thisNode.nodeID;
		boolean foundIconNextAction = false;
		boolean foundIconToday = false;
		
		
		// use index method to get attributes
		String naWhere = thisNode['Where'].toString();
		String naWho = thisNode['Who'].toString();
		String naWhen = thisNode['When'].toString();
			
		// take care of missing attributes. null or empty string evaluates as boolean false
		if (!naWho) {naWho = "tbd";}
		if (!naWhere) {naWhere = "_anywhere";}
		if (!naWhen) {naWhen = "This Week";}
		
		def result = [];
	
		// check for Next Action icon
		icons.each {
			if (it == iconNextAction){
				foundIconNextAction = true;
			}
		}
		
		// check for Today icon
		icons.each {
			if (it == iconToday){
				foundIconToday = true;
			}
		}
		
		// include result if it has next action icon and its not the icon setting node for next actions
		if (foundIconNextAction){
			if (!(naAction =~ /Icon:/)){
				def naProject = findNextActionProject(thisNode, listProjects);
				if (foundIconToday){naWhen = "Today";}
				result = [action:naAction, project:naProject, where:naWhere, who:naWho, when:naWhen, nodeID:naNodeID];
			}
		}
		
		thisNode.children.each {
							
			result += findNextActions(it, listProjects, iconNextAction, iconToday);
		}
		return result;
		
	}
	
	//--------------------------------------------------------------
	// 	Convert next action shorthand notation with recursive walk:
	//	shorthand: *<next action> @<where> [<who>] {<when>}
	//	becomes:
	// 			node.text     = <next action>
	//			node['Where'] = <where>
	//			node['Who']   = <who>
	//			node['When']  = <when>
	//
	public void ConvertShorthand(Proxy.Node thisNode){
		String nodeText = thisNode.text.trim();
		String[] field;
		
		if (nodeText.length()>0 && nodeText.charAt(0) == "*"){			
			field = parseShorthand(nodeText);			
			thisNode.text = field[0];
			def nodeAttr = [:];
			if (field[1]){nodeAttr["Where"]=field[1];}
			if (field[2]){nodeAttr["Who"]=field[2];}
			if (field[3]){nodeAttr["When"]=field[3];}
			thisNode.attributes = nodeAttr;
			//thisNode.attributes = ["Where":field[1], "Who":field[2], "When":field[3]];
			thisNode.icons.add(IconNextAction);	
		}
			
		thisNode.children.each {					
			ConvertShorthand(it);				
		}
	}
	
	//--------------------------------------------------------------
	// 	Parse next action shorthand notation
	//		field[0] = <next action>
	//		field[1] = <where>
	//		field[2] = <who>
	//		field[3] = <when>
	//
	private String[] parseShorthand(String nodeText){
		String[] field
		int posWho1 = nodeText.indexOf("[");
		int posWho2 = nodeText.indexOf("]");
		int posWhen1 = nodeText.indexOf("{");
		int posWhen2 = nodeText.indexOf("}");
		int posWhere = nodeText.indexOf("@");
		int posFirst;
		int posMax;		
		
		field = new String[4];
				
		// parse When
		if ((posWhen1>0)&&(posWhen2>0)){
			field[3] = nodeText.substring(posWhen1+1, posWhen2);
			field[3] = field[3].trim();
		}
		
		// parse Who
		if ((posWho1>0)&&(posWho2>0)){
			field[2] = nodeText.substring(posWho1+1, posWho2);
			field[2] = field[2].trim();
		}
		
		// parse Action
		posMax = nodeText.length();
		if (posWhen1==-1){posWhen1 = posMax;}
		if (posWho1==-1){posWho1 = posMax;}
		if (posWhere==-1){posWhere = posMax;}		
		posFirst = Math.min(posWhen1, posWho1);
		posFirst = Math.min(posFirst, posWhere);		
		field[0] = nodeText.substring(1,posFirst);
		field[0] = field[0].trim();
		
		// parse Where
		posWhere = nodeText.indexOf("@");
		if (posWhere>0){
			nodeText = nodeText.substring(posWhere);
			posWho1 = nodeText.indexOf("[");
			posWhen1 = nodeText.indexOf("{");
			posMax = nodeText.length();
			if (posWho1==-1){posWho1 = posMax;}
			if (posWhen1==-1){posWhen1 = posMax;}
			posFirst = Math.min(posWhen1, posWho1);
			field[1] = nodeText.substring(1,posFirst);
			field[1] = field[1].trim();
		}
				
		return field;
	}
		
	//--------------------------------------------------------------
	// parse the GTD mind map
	public void ParseMap(){
		// Get icon keys for next actions and projects
		IconNextAction = getNextActionIcon();
		IconProject = getProjectIcon();
		IconToday = getTodayIcon();
		
		// Expand any nodes with next action shorthand
		ConvertShorthand(RootNode);
		
		// Get project and next action lists
		ProjectList = getProjectList();
		NAList = getNAList();
		
		// Get HTML for next action lists
		ByProject = getHTMLByProject();
		ByWhere = getHTMLByWhere();
		ByWho = getHTMLByWho();
		ByWhen = getHTMLByWhen();
		
	}
	
}

//---------------------------------------------------------
// Refresh the GUI window
//---------------------------------------------------------
public class RefreshUIWindow implements ActionListener {

	private GTDReport report;
	
	public void actionPerformed(ActionEvent e) {
		report.Refresh();
	}
	
	public RefreshUIWindow(GTDReport gtdReport) {
		report = gtdReport;
	}
		
}

//---------------------------------------------------------
// Prints the GUI window
//---------------------------------------------------------
public class PrintUIWindow implements ActionListener {
	
	    GTDReport reportToPrint;
	    int reportNum = 0;
	    String strReport = "";
		
	    public void actionPerformed(ActionEvent e) {
		   
			// get currently selected tab
			reportNum = reportToPrint.TabIndex();
		   
			// get report
			switch (reportNum) {
				case 0: strReport = reportToPrint.ProjectReport(); break;
				case 1: strReport = reportToPrint.OwnerReport(); break;
				case 2: strReport = reportToPrint.ContextReport(); break;				
				case 3: strReport = reportToPrint.DueReport(); break;
				default: strReport = "(no report)"; break;
			}
		   
			JEditorPane panePrint = new JEditorPane("text/html", strReport);
			JTextComponent txtPrint = panePrint;
		 		   
			try {
				boolean complete = txtPrint.print();
				if (complete) {
				   // show a success message				
				} else {
				   // show a message indicating that printing was cancelled			
				}
			} catch (PrinterException pe) {
			   // Printing failed, report to the user			  
			}
		   
		}
	
		public PrintUIWindow(GTDReport gtdReport) {
			reportToPrint = gtdReport;   	   
		}
}

//---------------------------------------------------------
// Close the GUI window
//---------------------------------------------------------
public class CloseUIWindow implements ActionListener {
	
	   JFrame frameToClose;
	   
	   public void actionPerformed(ActionEvent e) {
		   frameToClose.setVisible(false);
		   frameToClose.dispose();			
	   }
	
	   public CloseUIWindow(JFrame f) {
		   frameToClose = f;
	   }
}

//---------------------------------------------------------
// Copy the GUI window
//---------------------------------------------------------
public class CopyUIWindow implements ActionListener {
	
	   GTDReport reportToCopy;
	   int reportNum = 0;
	   String strReport = "";
	   
	   public void actionPerformed(ActionEvent e) {		   
		   
		   // get currently selected tab
		   reportNum = reportToCopy.TabIndex();
		   
		   // get report
		   switch (reportNum) {
			   case 0: strReport = reportToCopy.ProjectReport(); break;
			   case 1: strReport = reportToCopy.OwnerReport(); break;
			   case 2: strReport = reportToCopy.ContextReport(); break;			   
			   case 3: strReport = reportToCopy.DueReport(); break;
			   default: strReport = "(no report)"; break;
		   }
		   
		   // copy to system clipboard as plain text
		   strReport = strReport.replaceAll("\\<.*?>","");		
		   StringSelection ss = new StringSelection(strReport);
		   Toolkit.getDefaultToolkit().getSystemClipboard().setContents(ss, null);
		   
	   }
	
	   public CopyUIWindow(GTDReport gtdReport) {
		   reportToCopy = gtdReport;		   
	   }
}


//---------------------------------------------------------
// Process hyperlink to map node
//---------------------------------------------------------
public class NodeLink implements HyperlinkListener {

	GTDReport report;
	Proxy.Controller ctrl;
		
	public void hyperlinkUpdate(HyperlinkEvent e){
		if (e.getEventType() == HyperlinkEvent.EventType.ACTIVATED){
			String linkNodeID = e.getDescription();			
			def nodesFound = ctrl.find{ it.nodeID == linkNodeID};
			if (nodesFound[0] != null){
				FoldToTop(nodesFound[0]);				
				UnfoldBranch(nodesFound[0]);
				ctrl.centerOnNode(nodesFound[0]);
				ctrl.select(nodesFound[0]);
			}
			else {
				UITools.informationMessage("Next Action not found in mind map. Refresh Next Action list");
			}
		}
	}

	// recursive unfolding of branch
	private void UnfoldBranch(Proxy.Node thisNode){
		Proxy.Node rootNode = thisNode.getMap().getRoot();
		if (thisNode != rootNode){
			thisNode.setFolded(false);
			UnfoldBranch(thisNode.getParent());
		}

	}

	// fold to first level
	private void FoldToTop(Proxy.Node thisNode){
		Proxy.Node rootNode = thisNode.getMap().getRoot();
		def Nodes = ctrl.findAll();
		Nodes.each { 
			it.setFolded(true); 
		}
		rootNode.setFolded(false);				 
	}

	
	public NodeLink(GTDReport gtdReport){
		report = gtdReport;
		ctrl = report.getController();
	}
}


//=========================================================
//	script
//=========================================================

// Select root node of map
Proxy.Node rootNode = node.map.root;
c.select(rootNode);

// create a GTDMapReader
GTDMapReader gtdMapReader = new GTDMapReader(rootNode);

// generate report GUI
GTDReport report = new GTDReport();
report.setUserPath(c.userDirectory.toString());
report.setController(c);
report.setMapReader(gtdMapReader);
report.Show();


