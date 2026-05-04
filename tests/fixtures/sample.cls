' sample.cls - class module fixture for extraction tests
Private m_name As String

Public Property Get Name() As String
    Name = m_name
End Property

Public Sub Initialize(name As String)
    m_name = name
End Sub

Public Function GetGreeting() As String
    GetGreeting = "Hello " & m_name
End Function
