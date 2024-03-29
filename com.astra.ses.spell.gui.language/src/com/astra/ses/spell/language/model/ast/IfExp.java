// Autogenerated AST node
package com.astra.ses.spell.language.model.ast;

import com.astra.ses.spell.language.model.SimpleNode;
import java.util.Arrays;

public final class IfExp extends exprType {
    public exprType test;
    public exprType body;
    public exprType orelse;

    public IfExp(exprType test, exprType body, exprType orelse) {
        this.test = test;
        this.body = body;
        this.orelse = orelse;
    }

    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + ((test == null) ? 0 : test.hashCode());
        result = prime * result + ((body == null) ? 0 : body.hashCode());
        result = prime * result + ((orelse == null) ? 0 : orelse.hashCode());
        return result;
    }

    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (obj == null)
            return false;
        if (getClass() != obj.getClass())
            return false;
        IfExp other = (IfExp) obj;
        if (test == null) {
            if (other.test != null)
                return false;
        } else if (!test.equals(other.test))
            return false;
        if (body == null) {
            if (other.body != null)
                return false;
        } else if (!body.equals(other.body))
            return false;
        if (orelse == null) {
            if (other.orelse != null)
                return false;
        } else if (!orelse.equals(other.orelse))
            return false;
        return true;
    }

    public IfExp createCopy() {
        return createCopy(true);
    }

    public IfExp createCopy(boolean copyComments) {
        IfExp temp = new IfExp(test != null ? (exprType) test.createCopy(copyComments) : null,
                body != null ? (exprType) body.createCopy(copyComments) : null,
                orelse != null ? (exprType) orelse.createCopy(copyComments) : null);
        temp.beginLine = this.beginLine;
        temp.beginColumn = this.beginColumn;
        if (this.specialsBefore != null && copyComments) {
            for (Object o : this.specialsBefore) {
                if (o instanceof commentType) {
                    commentType commentType = (commentType) o;
                    temp.getSpecialsBefore().add(commentType.createCopy(copyComments));
                }
            }
        }
        if (this.specialsAfter != null && copyComments) {
            for (Object o : this.specialsAfter) {
                if (o instanceof commentType) {
                    commentType commentType = (commentType) o;
                    temp.getSpecialsAfter().add(commentType.createCopy(copyComments));
                }
            }
        }
        return temp;
    }

    public String toString() {
        StringBuffer sb = new StringBuffer("IfExp[");
        sb.append("test=");
        sb.append(dumpThis(this.test));
        sb.append(", ");
        sb.append("body=");
        sb.append(dumpThis(this.body));
        sb.append(", ");
        sb.append("orelse=");
        sb.append(dumpThis(this.orelse));
        sb.append("]");
        return sb.toString();
    }

    public Object accept(VisitorIF visitor) throws Exception {
        return visitor.visitIfExp(this);
    }

    public void traverse(VisitorIF visitor) throws Exception {
        if (test != null) {
            test.accept(visitor);
        }
        if (body != null) {
            body.accept(visitor);
        }
        if (orelse != null) {
            orelse.accept(visitor);
        }
    }

}
