import "./TreeView.css";

// Libs
import React, { useState } from "react";

// 🔒 Kleines Icon-Komponent zur besseren Lesbarkeit
function ExpandCollapseIcon({ isExpanded, onClick }) {
    const iconArrow = isExpanded ? "icon-arrow-down" : "icon-arrow-right";

    return (
        <i
            className={`icon ${iconArrow} mr-1 cursor-pointer`}
            onClick={onClick}
        />
    );
}

// 🔒 Checkbox + Label-Zeile
const TreeItemLabel = ({
    node,
    isChecked,
    onToggleChecked,
    hasChildren,
    expanded,
    onToggleExpand,
}) => (
    <div className="bg-secondary d-flex d-flex-vertical-center">
        {hasChildren && (
            <ExpandCollapseIcon
                isExpanded={expanded}
                onClick={onToggleExpand}
            />
        )}
        <input
            className="mx-1 align-middle"
            type="checkbox"
            checked={isChecked}
            onChange={onToggleChecked}
        />
        <span>{node.label}</span>
    </div>
);

function TreeNode({ node }) {
    const [expanded, setExpanded] = useState(false);
    const [isChecked, setIsChecked] = useState(false);
    const hasChildren = node.children && node.children.length > 0;

    return (
        <li class="nav-item">
            <TreeItemLabel
                node={node}
                isChecked={isChecked}
                onToggleChecked={(e) => setIsChecked(e.target.checked)}
                hasChildren={hasChildren}
                expanded={expanded}
                onToggleExpand={() => setExpanded(!expanded)}
            />
            {hasChildren && expanded && (
                <ul class="nav">
                    {node.children.map((child) => (
                        <TreeNode key={child.id} node={child} />
                    ))}
                </ul>
            )}
        </li>
    );
}

function TreeView({ data }) {
    return (
        <div>
            <ul class="nav">
                {data.map((node) => (
                    <TreeNode key={node.id} node={node} />
                ))}
            </ul>
        </div>
    );
}

export default TreeView;
