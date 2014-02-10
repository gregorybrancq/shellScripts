// @ExecutionModes({ON_SELECTED_NODE, ON_SELECTED_NODE_RECURSIVELY})

// Find if the icon ok is already present
boolean hasIcons = false
hasIcons = icons.icons.contains("button_ok")

// Icon is not present
if (! hasIcons ) {
    // Find if the attribute Date is present
    boolean hasDate = false
    attrList = attributes.getAttributeNames()
    attrList.each {
        if ( it == "Date" ) {
            if ( node["Date"] != "" ) {
                hasDate = true
            }
        }
    }

    // Add date attribute
    if (! hasDate) {
        def today = new Date()
        def formattedDate = today.format('dd/MM/yy')
        node["Date"] = formattedDate
    }

    // Add ok icon
    node.icons.add("button_ok")
}

