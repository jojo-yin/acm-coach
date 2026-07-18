# Visualization Guide

Load when the user is stuck on a geometry, graph, or interval problem — or whenever Stage 2 (THINK) of Path A would benefit from a diagram. **Output the diagram inline in your response.** Do NOT create separate files.

## Decision: ASCII vs SVG

| Situation | Tool |
|-----------|------|
| Number line, intervals, simple array | **ASCII Art** — instant, no dependency |
| Tree / graph / flow (≤10 nodes) | **ASCII Art** — readable inline |
| Coordinate geometry, convex hull, polygon | **SVG** — precise shapes + labels |
| DP table, grid, matrix (small) | **ASCII Art** — tabular layout |
| Flowchart, decision tree, state machine | **ASCII Art** — box-and-arrow |

**Rule of thumb**: if you can draw it with keyboard characters in 10 seconds, use ASCII. If it needs precise shapes, angles, or curves, use SVG.

## ASCII Art Templates

### 1. Number Line + Intervals

For interval covering, scheduling, point selection.

```
Template (fill in {{placeholders}}):
```
```
{{label}}
{{intervals with |---| bars}}
----+----+----+----+----+----
{{scale numbers}}
{{annotations: chosen points, overlaps}}
```

Example — "选最少的点覆盖所有区间":
```
区间选点（按右端点排序后）:
[1,3]   |---|---|
[2,5]     |-------|
[4,6]         |---|
        ----------------
        0  1  2  3  4  5  6
选点:       ^           ^
           ans=1       ans=2
```

### 2. Binary Tree / Recursion Tree

```
        [0,4]
       /     \
    [0,2]    [3,4]
    /   \    /   \
 [0,1] [2] [3]  [4]
  / \
[0] [1]
```

### 3. Graph (Undirected / Directed)

Use monospace and simple edges.

```
   1 --- 2 --- 4
   |     |    /
   |     |   /
   3 --- 5
```

With edge weights:
```
   1 --5-- 2 --3-- 4
   |      |      /
   2      1     /
   |      |   /
   3 --4-- 5
```

### 4. DP Table / Grid

```
   0  1  2  3  4  5  (容量 j)
0  0  0  0  0  0  0
1  0  0  3  3  3  3   ← 物品1 (w=2, v=3)
2  0  0  3  4  4  7   ← 物品2 (w=3, v=4)
3  0  0  3  4  5  7   ← 物品3 (w=4, v=5)
```

### 5. Greedy Timeline / Scheduling

```
时间轴 →
0        5        10        15
|--------|---------|---------|
  A[0-3]    B[4-8]
     C[2-6]         D[9-13]
        冲突!         ✓
```

### 6. Monotonic Stack (Histogram)

```
高度
5 |         ██
4 |      ██ ██ ██
3 |   ██ ██ ██ ██ ██
2 |   ██ ██ ██ ██ ██
1 |██ ██ ██ ██ ██ ██
   -------------------
   0  1  2  3  4  5  6
   
栈变化: push→pop→push... (用文字描述即可)
```

### 7. Array / Prefix Sum

```
原数组: [3, 1, 4, 1, 5, 9, 2, 6]
前缀和: [3, 4, 8, 9,14,23,25,31]
         ↑           ↑
        l=0         r=4  → sum = 23-3 = 20
```

### 8. Two Pointers / Sliding Window

```
[2, 1, 5, 1, 3, 2], k=8
 L           R          sum=2+1+5+1=9 > 8
     L       R          sum=1+5+1+3=10 > 8 收缩L
         L   R          sum=5+1+3=9 > 8
            L R          sum=1+3+2=6 ≤ 8 ✓
```

## SVG Templates

Use for geometry problems. Output the SVG block directly — user can save as `.svg` and open in browser. **Keep dimensions ≤ 400×300 for reasonable inline display.**

### 9. Coordinate Plane (Geometry Base)

```svg
<svg width="360" height="260" xmlns="http://www.w3.org/2000/svg">
  <!-- Axes -->
  <line x1="40" y1="220" x2="340" y2="220" stroke="#333" stroke-width="1"/>
  <line x1="40" y1="220" x2="40" y2="20" stroke="#333" stroke-width="1"/>
  <!-- Grid (light) -->
  <g stroke="#eee" stroke-width="0.5">
    {{generate grid lines at intervals}}
  </g>
  <!-- Points / Shapes -->
  {{problem-specific geometry here}}
</svg>
```

### 10. Triangle with Circumcircle

```svg
<svg width="300" height="280" xmlns="http://www.w3.org/2000/svg">
  <!-- Triangle -->
  <polygon points="60,220 220,60 260,180" fill="rgba(100,149,237,0.1)" stroke="#4169E1" stroke-width="2"/>
  <!-- Vertices -->
  <circle cx="60" cy="220" r="4" fill="red"/>
  <text x="30" y="240" font-size="11" fill="#333">A</text>
  <circle cx="220" cy="60" r="4" fill="red"/>
  <text x="228" y="58" font-size="11" fill="#333">B</text>
  <circle cx="260" cy="180" r="4" fill="red"/>
  <text x="268" y="185" font-size="11" fill="#333">C</text>
  <!-- Circumcircle -->
  <circle cx="155" cy="145" r="90" fill="none" stroke="#DC143C" stroke-width="1.5" stroke-dasharray="6,3"/>
</svg>
```

### 11. Convex Hull

```svg
<svg width="350" height="250" xmlns="http://www.w3.org/2000/svg">
  <!-- All points (scatter) -->
  {{for each point: circle at (x, y)}}
  <!-- Hull polygon -->
  <polygon points="{{hull vertices}}" fill="rgba(100,149,237,0.15)" stroke="#4169E1" stroke-width="2"/>
  <!-- Interior points in lighter color -->
</svg>
```

### 12. Graph / Tree (when ASCII is insufficient)

```svg
<svg width="350" height="200" xmlns="http://www.w3.org/2000/svg">
  <!-- Nodes -->
  <circle cx="50" cy="100" r="18" fill="#E8F0FE" stroke="#4169E1" stroke-width="2"/>
  <text x="50" y="105" text-anchor="middle" font-size="13">1</text>
  <!-- More nodes... -->
  <!-- Edges (draw BEFORE nodes so they appear behind) -->
  <line x1="68" y1="96" x2="132" y2="56" stroke="#666" stroke-width="1.5"/>
  <!-- More edges... -->
</svg>
```

## Principles

1. **Inline, not separate files** — the diagram is part of the explanation. Don't make the user open another file.
2. **Annotate meaningfully** — every marker (^, ↑, ██, color) must have a text explanation beside it.
3. **Start simple** — a 3-line ASCII sketch that clarifies is worth more than a perfect SVG that takes 30 lines to write.
4. **Adapt to constraints** — if n=10, ASCII is fine. If n=10^5, draw a schematic, not the actual data.
5. **SVG colors** — use semantic colors: blue=structure, red=key insight, gray=background. Don't go overboard.
