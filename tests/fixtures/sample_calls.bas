' sample_calls.bas - call graph fixture for extract_vb6 tests
Public Function ComputeScore(data As Integer) As Integer
    ComputeScore = data * 2
End Function

Public Function Normalize(value As Double) As Double
    Normalize = value / 100.0
End Function

Public Function RunAnalysis(data As Integer) As Double
    Dim score As Integer
    score = ComputeScore(data)
    RunAnalysis = Normalize(score)
End Function
