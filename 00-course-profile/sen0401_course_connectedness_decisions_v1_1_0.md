# SEN0401 course T-Box 1.1.0: connectedness decisions (2026-10-19)

Before (1.0.0): 2 classes, 2 standing alone, 0 islands. After (1.1.0): 2 classes, 0 standing alone, 0 islands, 2 connected outward only.

| Property | Domain | Range | Source |
|---|---|---|---|
| sen0401:gapOfPart | PartGap | cme:CoursePart | PartGap comment: "A part the claimed course profile requires that this repository does not hold" |
| sen0401:gapInRepository | PartGap | cme:CourseRepository | same comment: "this repository does not hold" |
| sen0401:themeOfCourse | TermTheme | schema:Course | course A-Box: sen0401:Course (a schema:Course) carries cme:termTheme "Semantic technologies"; TermTheme_Fall2026 states it |

Not achieved: both classes are connected only outward. No relation between PartGap and TermTheme is supported by the course sources (the outline, README and A-Box tie a theme to the course and a gap to a required part, never one to the other), so none is invented. The owner decides whether a shared in-file class is wanted.
Link discovery: no candidates (two classes).
