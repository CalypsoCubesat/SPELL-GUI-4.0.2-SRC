// Autogenerated AST node
package com.astra.ses.spell.language.model.ast;

import com.astra.ses.spell.language.model.SimpleNode;
import java.util.Arrays;

public final class Assert extends stmtType {
    public exprType test;
    public exprType msg;

    public Assert(exprType test, exprType msg) {
        this.test = test;
        this.msg = msg;
    }

    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + ((test == null) ? 0 : test.hashCode());
        result = prime * result + ((msg == null) ? 0 : msg.hashCode());
        return result;
    }

    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (obj == null)
            return false;
        if (getClass() != obj.getClass())
            return false;
        Assert other = (Assert) obj;
        if (test == null) {
            if (other.test != null)
                return false;
        } else if (!test.equals(other.test))
            return false;
        if (msg == null) {
            if (other.msg != null)
                return false;
        } else if (!msg.equals(other.msg))
            return false;
        return true;
    }

    public Assert createCopy() {
        return createCopy(true);
    }

    public Assert createCopy(boolean copyComments) {
        Assert temp = new Assert(test != null ? (exprType) test.createCopy(copyComments) : null,
                msg != null ? (exprType) msg.createCopy(copyComments) : null);
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
        StringBuffer sb = new StringBuffer("Assert[");
        sb.append("test=");
        sb.append(dumpThis(this.test));
        sb.append(", ");
        sb.append("msg=");
        sb.append(dumpThis(this.msg));
        sb.append("]");
        return sb.toString();
    }

    public Object accept(VisitorIF visitor) throws Exception {
        return visitor.visitAssert(this);
    }

    public void traverse(VisitorIF visitor) throws Exception {
        if (test != null) {
            test.accept(visitor);
        }
        if (msg != null) {
            msg.accept(visitor);
        }
    }

}
