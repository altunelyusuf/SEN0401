"""Builds the two demo covers (SEN0401 and SEN0414) with the renderer v1.0.0. The question-to-outcome assignment is a DEMONSTRATION only: the real assignment comes with the paper."""
import sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import sen0401_exam_cover_render_v1_0_0 as c
out='/home/claude/sen0401/08-tooling/exam/'
qs=[('1',25,False),('2',25,False),('3',25,False),('4',25,False),('5',10,True)]
d=c.new_document()
c.cover(d,'SEN0401','Special Topics: Blockchain','Midterm Exam','Fall','2026-2027',None,'60 Minutes','Dr. Yusuf ALTUNEL',qs,
 [[1,9],[2,6],[3,4],[5,6],[1,2]],outcomes_ttl='/home/claude/sen0401/01-outcomes/sen0401_outcomes_v1_1_1.ttl')
d.save(out+'sen0401_exam_cover_demo_v1_0_0.docx')
d=c.new_document()
c.cover(d,'SEN0414','Advanced Programming','Midterm Exam','Fall','2026-2027',None,'60 Minutes','Dr. Yusuf ALTUNEL',qs,
 [[1,2],[3,5],[4,6],[7],[1,6]],outcomes_ttl='/home/claude/AdvancedProgrammingWithPython/01-outcomes/sen0414_outcomes_v1_0_0.ttl')
d.save(out+'sen0401_exam_cover_demo_sen0414_v1_0_0.docx')
