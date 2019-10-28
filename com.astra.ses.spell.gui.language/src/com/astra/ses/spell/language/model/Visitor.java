/**
 * Copyright (c) 2005-2011 by Appcelerator, Inc. All Rights Reserved.
 * Licensed under the terms of the Eclipse Public License (EPL).
 * Please see the license.txt included with this distribution for details.
 * Any modifications to this file must keep this entire header intact.
 */
package com.astra.ses.spell.language.model;

import com.astra.ses.spell.language.model.ast.VisitorBase;

public class Visitor extends VisitorBase {

    /**
     * Visit each of the children one by one.
     * @args node The node whose children will be visited.
     */
    public void traverse(SimpleNode node) throws Exception {
        node.traverse(this);
    }

    public void visit(SimpleNode[] nodes) throws Exception {
        for (int i = 0; i < nodes.length; i++) {
            visit(nodes[i]);
        }
    }

    /**
     * Visit the node by calling a visitXXX method.
     */
    public Object visit(SimpleNode node) throws Exception {
        open_level(node);
        Object ret = node.accept(this);
        close_level(node);
        return ret;
    }

    protected Object unhandled_node(SimpleNode node) throws Exception {
        return this;
    }

    protected void open_level(SimpleNode node) throws Exception {
    }

    protected void close_level(SimpleNode node) throws Exception {
    }
}
