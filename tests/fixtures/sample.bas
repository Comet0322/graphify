' sample.bas - basic module fixture for extraction tests
Public Function Add(a As Integer, b As Integer) As Integer
    Add = a + b
End Function

Public Function Multiply(a As Integer, b As Integer) As Integer
    Multiply = a * b
End Function

Public Sub PrintResult(result As Integer)
    MsgBox CStr(result)
End Sub
