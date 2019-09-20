VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} ExportToolv2 
   Caption         =   "MapAction Export Tool v2"
   ClientHeight    =   8220
   ClientLeft      =   45
   ClientTop       =   435
   ClientWidth     =   5190
   OleObjectBlob   =   "ExportToolv2.2.frx":0000
   StartUpPosition =   1  'CenterOwner
End
Attribute VB_Name = "ExportToolv2"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False



Option Explicit
  ' original script variables
  Dim pMxDoc As IMxDocument
  Dim pMap As IMap
  Dim pGxDialog As IGxDialog
  Dim pGxObjectFilter As IGxObjectFilter
  Dim anythingSelected As Boolean
  Dim pGxFolders As IEnumGxObject
  Dim pGxFolder As IGxObject
  Dim strStartingLocation As String
  Dim pdfFullPathName As String
  Dim jpgFullPathName As String
  Dim response
  Dim pGxObject As IGxObject
  Dim pPageLayout As IPageLayout
  Dim pAV As IActiveView
  Dim blnEmbedFonts As Boolean
  Dim blnPolygonizeMarkers As Boolean
  Dim pExporter As IExport
  Dim pExportPDF As IExportPDF
  Dim pExportJPEG As IExportJPEG
  Dim pExportVectorOptions As IExportVectorOptions
  Dim tExpRect As tagRECT
  Dim hDC As Long
  Dim dWidth As Double, dHeight As Double
  Dim pEnv As IEnvelope
  
  ' added by mike
  
  Dim workingDir As String
  Dim mxdName As String
  Dim mxdRoot As String
  Dim thisDoc As String
  Dim jpgFileLen As Long
  Dim pdfFileLen As Long
  Dim operationID As Integer


Public Sub UserForm_Initialize()

' always open on the main window
Multipage.Value = 0

' hardcode operationID if required, just uncomment
'operationID = 999

' get current MXD name
thisDoc = Application.Templates.Item(Application.Templates.Count - 1)
txt_thisMXD.Text = thisDoc

' set pMxDoc to thisDoc
Set pMxDoc = Application.Document

' get doc names and folders
workingDir = Left(thisDoc, InStrRev(thisDoc, "\"))
mxdName = Right(thisDoc, Len(thisDoc) - InStrRev(thisDoc, "\"))
mxdRoot = Left(mxdName, InStrRev(mxdName, ".") - 1)
strStartingLocation = workingDir

drop_status.AddItem "New"
drop_status.AddItem "Correction"
drop_status.AddItem "Update"

drop_qclevel.AddItem "Checked by MapAction"
drop_qclevel.AddItem "Not checked"

drop_access.AddItem "Public"
drop_access.AddItem "Humanitarian"
drop_access.AddItem "MapAction"


' set up ArcObject variables
Dim pGraphicsContainer As IGraphicsContainer
Dim element As IElement, textElement As ITextElement
Dim elementProps As IElementProperties
Set pPageLayout = pMxDoc.PageLayout
Set pAV = pPageLayout
Set pGraphicsContainer = pAV
pGraphicsContainer.Reset

' get metadata from map and populate form
Set element = pGraphicsContainer.Next
Do While Not element Is Nothing
    If TypeOf element Is ITextElement Then
        Set elementProps = element
        Set textElement = element
        If elementProps.Name = "title" Then
            txt_title.Text = Replace(Replace(textElement.Text, vbCrLf, " "), "  ", " ")
        ElseIf elementProps.Name = "scaleString" Then
            ' need to split it up
            Dim scaleString() As String, s1 As String, s2 As String, c As Integer
            scaleString = Split(textElement.Text, " ", 10)
            ' guess which element is which!
            If UBound(scaleString) >= 2 Then
                If scaleString(1) = "1:" Then s1 = scaleString(1) & scaleString(2)
                If (Left(scaleString(1), 2) = "1:") And (Len(scaleString(1)) > 4) Then s1 = scaleString(1)
                If Len(scaleString(2)) = 2 And Left(scaleString(2), 1) = "A" Then s2 = UCase(scaleString(2))
            End If
            If UBound(scaleString) >= 2 Then
                If scaleString(0) = "1:" Then s1 = scaleString(0) & scaleString(1)
                If (Left(scaleString(0), 2) = "1:") And (Len(scaleString(0)) > 4) Then s1 = scaleString(0)
                If Len(scaleString(2)) = 2 And Left(scaleString(2), 1) = "A" Then s2 = UCase(scaleString(2))
            End If
            If UBound(scaleString) >= 3 Then
                If Len(scaleString(3)) = 2 And Left(scaleString(3), 1) = "A" Then s2 = UCase(scaleString(3))
            End If
            If UBound(scaleString) >= 4 Then
                If Len(scaleString(4)) = 2 And Left(scaleString(4), 1) = "A" Then s2 = UCase(scaleString(4))
            End If
          
            txt_scale.Text = s1
            txt_papersize.Text = s2
            
        ElseIf elementProps.Name = "ref" Then
            txt_ref.Text = Trim(textElement.Text)
            'list_status.Value = "New"
            'If Right(Trim(textElement.Text), 2) = "v1" Then list_status.Value = "New"
            'If Right(Trim(textElement.Text), 2) <> "v1" Then list_status.Value = "Update"
        ElseIf elementProps.Name = "summary" Then
            txt_summary.Text = Replace(Replace(textElement.Text, vbCrLf, " "), "  ", " ")
            
        ElseIf elementProps.Name = "datetimeString" Then
            ' need to reformat date
            Dim datetimeString() As String
            datetimeString = Split(textElement.Text, "/", 20)
            txt_createdate.Text = Format(Trim(datetimeString(0)), "yyyy-mm-dd")
            txt_createtime.Text = Trim(datetimeString(1))
        ElseIf elementProps.Name = "projdatumString" Then
            Dim projdatumString() As String
            projdatumString = Split(textElement.Text, "/", 50)
            txt_proj = Trim(projdatumString(0))
            txt_datum = Trim(projdatumString(1))
        ElseIf elementProps.Name = "glideno" Then
            txt_glideno.Text = Trim(textElement.Text)
        ElseIf elementProps.Name = "datasourceString" Then
        Dim textHolder As String
        textHolder = Replace(Replace(textElement.Text, vbCrLf, " "), "  ", " ")
        txt_datasource.Text = Trim(Replace(textHolder, "<bol>Data sources:</bol>", ""))
        
        End If
    End If
    Set element = pGraphicsContainer.Next
Loop

' set operationID if hardcoded above
txt_operationID = operationID

End Sub

Public Sub cmb_Output_Click()

' opens dialog box for output location
Set pGxObjectFilter = New GxFilterBasicTypes
Set pGxDialog = New GxDialog
With pGxDialog
    .Title = "Select output folder for export..."
    .StartingLocation = strStartingLocation
End With
Set pGxDialog.ObjectFilter = pGxObjectFilter
anythingSelected = pGxDialog.DoModalOpen(Application.hwnd, pGxFolders)

If anythingSelected Then
    Set pGxFolder = pGxFolders.Next
Else
    MsgBox "Please reselect output folder"
    Exit Sub
End If

' adding location to text box
txt_Output.Text = pGxFolder.FullName
End Sub

Public Sub cmb_Options_Click()

' this opens the multipage tab according to the user choice
Multipage.Value = 2

End Sub
Public Sub cmb_back1_Click()

' this opens the multipage tab according to the user choice
Multipage.Value = 0

End Sub
Public Sub cmb_back2_Click()

' this opens the multipage tab according to the user choice
Multipage.Value = 0

End Sub
Public Sub cmb_back3_Click()

' this opens the multipage tab according to the user choice
Multipage.Value = 0

End Sub
Public Sub cmb_moreMetadata_Click()

' this opens the multipage tab according to the user choice
Multipage.Value = 1

End Sub

Public Sub cmb_Export_Click()

Dim pMouseCursor As IMouseCursor
Set pMouseCursor = New MouseCursor
' this sets the cursor to an hourglass
pMouseCursor.SetCursor 2
  
Set pMxDoc = Application.Document
Set pPageLayout = pMxDoc.PageLayout
Set pAV = pMxDoc.FocusMap

' do some calculations for paper edge coords
Dim pGraphicsContainer As IGraphicsContainer
Dim pMapFrame As IMapFrame
Dim pMapFrameProps As IElement
Dim extentXMax As Double
Dim extentXMin As Double
Dim extentYMax As Double
Dim extentYMin As Double
Dim pageXMax As Double
Dim pageXMin As Double
Dim pageYMax As Double
Dim pageYMin As Double
Dim pageHeight As Double
Dim pageWidth As Double
Dim frameHeight As Double
Dim frameWidth As Double
Dim frameXMin As Double
Dim frameYMin As Double

Set pGraphicsContainer = pPageLayout
Set pMapFrame = pGraphicsContainer.FindFrame(pMxDoc.Maps.Item(0))
Set pMapFrameProps = pMapFrame

' check map projection, only compute extent data if a geographic projection
Dim mapUnits As String

mapUnits = pMapFrame.Map.SpatialReference.Name
If Left(mapUnits, 4) = "GCS_" Then
    extentXMax = pAV.Extent.Envelope.XMax
    extentXMin = pAV.Extent.Envelope.XMin
    extentYMax = pAV.Extent.Envelope.YMax
    extentYMin = pAV.Extent.Envelope.YMin
    pageHeight = pPageLayout.Page.PrintableBounds.Height
    pageWidth = pPageLayout.Page.PrintableBounds.Width
    frameHeight = pMapFrameProps.Geometry.Envelope.Height
    frameWidth = pMapFrameProps.Geometry.Envelope.Width
    frameXMin = pMapFrameProps.Geometry.Envelope.XMin
    frameYMin = pMapFrameProps.Geometry.Envelope.YMin
    pageXMin = extentXMin - (((extentXMax - extentXMin) / frameWidth) * frameXMin)
    pageXMax = extentXMax + (((extentXMax - extentXMin) / frameWidth) * (pageWidth - (frameXMin + frameWidth)))
    pageYMin = extentYMin - (((extentYMax - extentYMin) / frameHeight) * frameYMin)
    pageYMax = extentYMax + (((extentYMax - extentYMin) / frameHeight) * (pageHeight - (frameYMin + frameHeight)))

Else
  MsgBox "Map projection is " & mapUnits & ", extent data can not be extracted", vbInformation, "Projection"
End If

' do some error checking now ...
Dim errorMessage As String, errorMessage1 As String
errorMessage = ""
errorMessage1 = ""

If txt_Output.Text = "" Then
    errorMessage1 = "Please select output folder" & vbCrLf
End If

If txt_operationID = "" Then
    errorMessage = errorMessage & "  Please enter an operation ID, 0 is allowed" & vbCrLf
Else
    If Not IsNumeric(txt_operationID) Then
        errorMessage = errorMessage & "  Please enter a numeric operation ID" & vbCrLf
    End If

End If

If txt_title.Text = "" Then
    errorMessage = errorMessage & "  Please enter a map title" & vbCrLf
End If

If txt_ref.Text = "" Then
    errorMessage = errorMessage & "  Please enter a map reference" & vbCrLf
End If

If txt_proj.Text = "" Then
    errorMessage = errorMessage & "  Please enter a map projection (e.g. UTM 42N)" & vbCrLf
End If

If txt_datum.Text = "" Then
    errorMessage = errorMessage & "  Please enter a map datum (e.g. WGS84)" & vbCrLf
End If

If txt_createdate.Text = "" Then
    errorMessage = errorMessage & "  Please enter a date (YYYY-MM-DD)" & vbCrLf
End If

If txt_createtime.Text = "" Then
    errorMessage = errorMessage & "  Please enter a time (hh:mm)" & vbCrLf
End If

If drop_status.Value = "" Then
    errorMessage = errorMessage & "  Please select map status" & vbCrLf
End If

If drop_qclevel.Value = "" Then
    errorMessage = errorMessage & "  Please select map qclevel" & vbCrLf
End If

If drop_access.Value = "" Then
    errorMessage = errorMessage & "  Please select map access" & vbCrLf
End If

If errorMessage <> "" Then
    errorMessage = vbCrLf & "Essential metadata are missing!" & vbCrLf & errorMessage
End If

errorMessage = errorMessage1 & errorMessage

If errorMessage <> "" Then
    MsgBox errorMessage, vbExclamation, "Warning"
    Multipage.Value = 0
    Exit Sub
End If

' lets do PDF first ...

' picking up the user specified output resolution
If txt_OutputResPDF = "" Then
    MsgBox "Please enter a PDF output resolution", vbExclamation, "Warning"
    Multipage.Value = 2
    txt_OutputResPDF.SetFocus
    Exit Sub
End If

If Not IsNumeric(txt_OutputResPDF) Then
    MsgBox "Please enter numeric PDF output resolution", vbExclamation, "Warning"
    Multipage.Value = 2
    txt_OutputResPDF.SetFocus
    Exit Sub
End If

If txt_OutputResPDF < 96 Then
    MsgBox "Please enter a PDF dpi resolution between 96 and 1200", vbExclamation, "Warning"
    Multipage.Value = 2
    txt_OutputResPDF.SetFocus
    Exit Sub
End If

If txt_OutputResPDF > 1200 Then
    MsgBox "Please enter a PDF dpi resolution between 96 and 1200", vbExclamation, "Warning"
    Multipage.Value = 2
    txt_OutputResPDF.SetFocus
    Exit Sub
End If

' picking up the output resolution for PDFs
Dim lngOutputResolutionPDF As Long, filenamePDF As String
lngOutputResolutionPDF = txt_OutputResPDF.Text

' picking up whether the user wishes to embed document fonts
If cb_EmbedFonts.Value = True Then
    blnEmbedFonts = True
Else
    blnEmbedFonts = False
End If

' picking up whether the user wishes to convert marker symbols to polygons
If cb_ConvertMarker.Value = True Then
    blnPolygonizeMarkers = True
Else
    blnPolygonizeMarkers = False
End If

With Application.StatusBar.ProgressBar
    .Message = "Exporting MXD to PDF..."
    .MinRange = 0
    .MaxRange = 1
    .StepValue = 1
    .Show
End With

filenamePDF = mxdRoot & "-" & txt_OutputResPDF & "dpi.pdf"
pdfFullPathName = pGxFolder.FullName & "\" & filenamePDF
    
' export time....
If PDFExists(pdfFullPathName) = True Then
    response = MsgBox(pdfFullPathName & " already exists. Replace it?", vbYesNo)
    If response = vbYes Then
        CreatePDF pPageLayout, pdfFullPathName, lngOutputResolutionPDF, blnEmbedFonts, blnPolygonizeMarkers
    End If
Else
    CreatePDF pPageLayout, pdfFullPathName, lngOutputResolutionPDF, blnEmbedFonts, blnPolygonizeMarkers
End If
    
pdfFileLen = FileLen(pdfFullPathName) 'for metadata later

' now do jpg
  
' error checking

If txt_OutputResJPEG = "" Then
    MsgBox "ATTENTION: please enter a JPG output resolution", vbExclamation, "Warning"
    Multipage.Value = 2
    txt_OutputResJPEG.SetFocus
    Exit Sub
End If

If Not IsNumeric(txt_OutputResJPEG) Then
    MsgBox "ATTENTION: please enter numeric JPG output resolution", vbExclamation, "Warning"
    Multipage.Value = 2
    txt_OutputResJPEG.SetFocus
    Exit Sub
End If

If txt_OutputResJPEG < 96 Then
    MsgBox "ATTENTION: please enter a JPG dpi resolution between 96 and 1200", vbExclamation, "Warning"
    Multipage.Value = 2
    txt_OutputResJPEG.SetFocus
    Exit Sub
End If

If txt_OutputResJPEG > 1200 Then
    MsgBox "ATTENTION: please enter a JPG dpi resolution between 96 and 1200", vbExclamation, "Warning"
    Multipage.Value = 2
    txt_OutputResJPEG.SetFocus
    Exit Sub
End If

' picking the output resolution for JPEGs
Dim lngOutputResolutionJPEG As Long, filenameJPEG As String
lngOutputResolutionJPEG = txt_OutputResJPEG.Text
  
' progress bar
  With Application.StatusBar.ProgressBar
    .Message = "Exporting MXD to JPEG..."
    .MinRange = 0
    .MaxRange = 1
    .StepValue = 1
    .Show
  End With
    
filenameJPEG = mxdRoot & "-" & txt_OutputResJPEG & "dpi.jpg"
jpgFullPathName = pGxFolder.FullName & "\" & filenameJPEG
  
' do the export
If JPEGExists(jpgFullPathName) = True Then
    response = MsgBox(jpgFullPathName & " already exists. Replace it?", vbYesNo)
    If response = vbYes Then
        CreateJPEG pPageLayout, jpgFullPathName, lngOutputResolutionJPEG
    End If
Else
    CreateJPEG pPageLayout, jpgFullPathName, lngOutputResolutionJPEG
End If
    
jpgFileLen = FileLen(jpgFullPathName) 'for metadata later
   
' OK, now do XML file ...
Dim XMLFileName As String, filenameXML As String
filenameXML = mxdRoot & ".xml"
XMLFileName = pGxFolder.FullName & "\" & filenameXML

' progress bar
  With Application.StatusBar.ProgressBar
    .Message = "Exporting Metadata as XML..."
    .MinRange = 0
    .MaxRange = 1
    .StepValue = 1
    .Show
  End With


' open file for writing
Dim objFSO
Dim objTextStream
Set objFSO = CreateObject("Scripting.FileSystemObject")
objFSO.CreateTextFile XMLFileName, True 'create file
Set objTextStream = objFSO.OpenTextFile(XMLFileName, 2, True) 'open file

' now write the xml
objTextStream.WriteLine "<?xml version=""1.0"" encoding=""iso-8859-1""?>"
objTextStream.WriteLine "<mapdoc>"
objTextStream.WriteLine "  <mapdata>"
objTextStream.WriteLine "    <!-- essential tags -->"
objTextStream.WriteLine "    <operationID>" & txt_operationID & "</operationID>"
objTextStream.WriteLine "    <sourceorg>MapAction</sourceorg>"
objTextStream.WriteLine "    <title><![CDATA[" & txt_title & "]]></title>"
objTextStream.WriteLine "    <ref>" & txt_ref & "</ref>"
objTextStream.WriteLine "    <language>" & txt_language & "</language>"
objTextStream.WriteLine "    <countries><![CDATA[" & txt_countries & "]]></countries>"
objTextStream.WriteLine "    <createdate>" & txt_createdate & "</createdate>"
objTextStream.WriteLine "    <createtime>" & txt_createtime & "</createtime>"
objTextStream.WriteLine "    <status>" & drop_status.Value & "</status>"
objTextStream.WriteLine "    <xmax>" & Round(extentXMax, 4) & "</xmax>"
objTextStream.WriteLine "    <xmin>" & Round(extentXMin, 4) & "</xmin>"
objTextStream.WriteLine "    <ymax>" & Round(extentYMax, 4) & "</ymax>"
objTextStream.WriteLine "    <ymin>" & Round(extentYMin, 4) & "</ymin>"
objTextStream.WriteLine "    <proj><![CDATA[" & txt_proj & "]]></proj>"
objTextStream.WriteLine "    <datum><![CDATA[" & txt_datum & "]]></datum>"
objTextStream.WriteLine "    <jpgfilename>" & filenameJPEG & "</jpgfilename>"
objTextStream.WriteLine "    <pdffilename>" & filenamePDF & "</pdffilename>"
objTextStream.WriteLine "    <qclevel>" & drop_qclevel.Value & "</qclevel>"
objTextStream.WriteLine "    <qcname><![CDATA[" & txt_qcname & "]]></qcname>"
objTextStream.WriteLine "    <access>" & drop_access.Value & "</access>"
objTextStream.WriteLine "    <!-- optional tags -->"
objTextStream.WriteLine "    <glideno>" & txt_glideno & "</glideno>"
objTextStream.WriteLine "    <summary><![CDATA[" & txt_summary & "]]></summary>"
objTextStream.WriteLine "    <imagerydate>" & txt_imagerydate & "</imagerydate>"
objTextStream.WriteLine "    <datasource><![CDATA[" & txt_datasource & "]]></datasource>"
objTextStream.WriteLine "    <location><![CDATA[" & txt_location & "]]></location>"
objTextStream.WriteLine "    <theme><![CDATA[" & txt_theme & "]]></theme>"
objTextStream.WriteLine "    <scale>" & txt_scale & "</scale>"
objTextStream.WriteLine "    <papersize>" & txt_papersize & "</papersize>"
objTextStream.WriteLine "    <jpgfilesize>" & jpgFileLen & "</jpgfilesize>"
objTextStream.WriteLine "    <jpgresolutiondpi>" & txt_OutputResJPEG & "</jpgresolutiondpi>"
objTextStream.WriteLine "    <pdffilesize>" & pdfFileLen & "</pdffilesize>"
objTextStream.WriteLine "    <pdfresolutiondpi>" & txt_OutputResPDF & "</pdfresolutiondpi>"
objTextStream.WriteLine "    <mxdfilename>" & mxdRoot & ".mxd</mxdfilename>"
objTextStream.WriteLine "    <paperxmax>" & Round(pageXMax, 4) & "</paperxmax>"
objTextStream.WriteLine "    <paperxmin>" & Round(pageXMin, 4) & "</paperxmin>"
objTextStream.WriteLine "    <paperymax>" & Round(pageYMax, 4) & "</paperymax>"
objTextStream.WriteLine "    <paperymin>" & Round(pageYMin, 4) & "</paperymin>"
objTextStream.WriteLine "    <kmzfilename>" & txt_kmzfilename & "</kmzfilename>"
objTextStream.WriteLine "    <accessnotes><![CDATA[" & txt_accessnotes & "]]></accessnotes>"
objTextStream.WriteLine "  </mapdata>"
objTextStream.WriteLine "</mapdoc>"

' close file
objTextStream.Close
Set objTextStream = Nothing
Set objFSO = Nothing

With Application.StatusBar.ProgressBar
    .Message = "Waiting..."
    .MinRange = 0
    .MaxRange = 1
    .StepValue = 1
    .Show
End With

'wait 2 seconds while xml file closes, sometimes the zip routine gets ahead
Dim t As Double
t = Now() + 2 / 86400#
While t > Now()
  DoEvents
Wend

' and finally, zip whole lot up
Dim sFName As String
Dim oApp As Object, iCtr As Long, I As Integer
Dim FName(2) As Variant, vArr, FileNameZip

' progress bar
  With Application.StatusBar.ProgressBar
    .Message = "Zipping it all up..."
    .MinRange = 0
    .MaxRange = 1
    .StepValue = 1
    .Show
  End With

FileNameZip = pGxFolder.FullName & "\" & mxdRoot & ".zip"
FName(0) = pGxFolder.FullName & "\" & filenamePDF
FName(1) = pGxFolder.FullName & "\" & filenameJPEG
FName(2) = pGxFolder.FullName & "\" & filenameXML

'Create empty zip
NewZip (FileNameZip)
Set oApp = CreateObject("Shell.Application")
I = 0
For iCtr = LBound(FName) To UBound(FName)
  I = I + 1
  oApp.Namespace(FileNameZip).CopyHere FName(iCtr)
  ' this delay script below commented out as script hanging with it in
  On Error Resume Next
  Do Until oApp.Namespace(FileNameZip).Items.Count = I
    Application.Wait (Now + TimeValue("0:00:01"))
  Loop
  On Error GoTo 0
Next iCtr
  
  ' Hide progressbar
  Application.StatusBar.ProgressBar.Hide
  
  MsgBox "Export Complete!"
  Unload Me
  
End Sub

Private Function PDFExists(sFullPathName As String) As Boolean
  
  Dim MyFile
 
  MyFile = Dir(sFullPathName)
  If MyFile = "" Then
    PDFExists = False
  Else
    PDFExists = True
  End If
  
End Function

Private Sub CreatePDF( _
  pPageLayout As IPageLayout, _
  sFullPathName As String, _
  lngOutputResolutionPDF As Long, _
  blnEmbedFonts As Boolean, _
  blnPolygonizeMarkers As Boolean)
  
    Dim pActiveView As IActiveView
    Dim pPixelBoundsEnvPDF As IEnvelope
    Dim exportRECTPDF As tagRECT
    
    '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Set pActiveView = pPageLayout
    '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Set pExporter = New ExportPDF
    
    'This code is specifically for PDF exporting
    '#############################################################################
    Dim pExportPDF As IExportPDF
    Set pExportPDF = pExporter
    
    With pExportPDF
        .Compressed = True
        .EmbedFonts = blnEmbedFonts
        .ImageCompression = esriExportImageCompressionDeflate
    End With
    '##############################################################################
    
    Dim iScreenResolutionPDF As Integer
    iScreenResolutionPDF = 96
  
    With exportRECTPDF
        .Left = 0
        .Top = 0
        .Right = pActiveView.ExportFrame.Right * (lngOutputResolutionPDF / iScreenResolutionPDF)
        .bottom = pActiveView.ExportFrame.bottom * (lngOutputResolutionPDF / iScreenResolutionPDF)
    End With
    
    Set pPixelBoundsEnvPDF = New Envelope
    pPixelBoundsEnvPDF.PutCoords exportRECTPDF.Left, exportRECTPDF.Top, exportRECTPDF.Right, exportRECTPDF.bottom
    pExporter.PixelBounds = pPixelBoundsEnvPDF
    
    ' exporter object
    With pExporter
      .PixelBounds = pPixelBoundsEnvPDF
      .Resolution = lngOutputResolutionPDF
      .ExportFileName = sFullPathName
    End With
    
    '"Set pActiveView = pPageLayout" is the vital piece of code to pick up all MXDs
    hDC = pExporter.StartExporting
    
    '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    SetOutputQuality pActiveView, 1
    '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    pActiveView.Output hDC, pExporter.Resolution, exportRECTPDF, Nothing, Nothing
    pExporter.FinishExporting
    DoEvents
    pExporter.Cleanup
    
    'Clear out the variables.
    Set pExporter = Nothing
    Set pActiveView = Nothing
    Set pMxDoc = Nothing
  
End Sub

Private Function JPEGExists(sFullPathName As String) As Boolean
  
  Dim MyFile
 
  MyFile = Dir(sFullPathName)
  If MyFile = "" Then
    JPEGExists = False
  Else
    JPEGExists = True
  End If
  
End Function

Private Sub CreateJPEG( _
  pPageLayout As IPageLayout, _
  sFullPathName As String, _
  lngOutputResolutionJPEG As Long)
  
    Dim pActiveView As IActiveView
    Dim pPixelBoundsEnvJPEG As IEnvelope
    Dim exportRECTJPEG As tagRECT

    '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Set pActiveView = pPageLayout
    '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Set pExporter = New ExportJPEG
    
    Dim iScreenResolutionJPEG As Integer
    iScreenResolutionJPEG = 96
  
    With exportRECTJPEG
        .Left = 0
        .Top = 0
        .Right = pActiveView.ExportFrame.Right * (lngOutputResolutionJPEG / iScreenResolutionJPEG)
        .bottom = pActiveView.ExportFrame.bottom * (lngOutputResolutionJPEG / iScreenResolutionJPEG)
    End With
    
    Set pPixelBoundsEnvJPEG = New Envelope
    pPixelBoundsEnvJPEG.PutCoords exportRECTJPEG.Left, exportRECTJPEG.Top, exportRECTJPEG.Right, exportRECTJPEG.bottom
    pExporter.PixelBounds = pPixelBoundsEnvJPEG
    
    ' exporter object
    With pExporter
      .PixelBounds = pPixelBoundsEnvJPEG
      .Resolution = lngOutputResolutionJPEG
      .ExportFileName = sFullPathName
    End With
    
    '"Set pActiveView = pPageLayout" is the vital piece of code to pick up all MXDs
    hDC = pExporter.StartExporting
    
    '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    SetOutputQuality pActiveView, 1
    '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    pActiveView.Output hDC, pExporter.Resolution, exportRECTJPEG, Nothing, Nothing
    pExporter.FinishExporting
    DoEvents
    pExporter.Cleanup
    
    'Clear out the variables.
    Set pExporter = Nothing
    Set pActiveView = Nothing
    Set pMxDoc = Nothing
      
End Sub

Private Function PageExtent(pPageLayout As IPageLayout) As IEnvelope
'    Dim dWidth As Double, dHeight As Double
    pPageLayout.Page.QuerySize dWidth, dHeight
'    Dim pEnv As IEnvelope
    Set pEnv = New Envelope
    pEnv.PutCoords 0#, 0#, dWidth, dHeight
    Set PageExtent = pEnv
End Function

Private Sub SetOutputQuality(pActiveView As IActiveView, lOutputQuality As Long)

    'Assign ResampleRatio
    Dim pOutputRasterSettings As IOutputRasterSettings
    Set pOutputRasterSettings = pActiveView.ScreenDisplay.DisplayTransformation
    pOutputRasterSettings.ResampleRatio = lOutputQuality
  
    If TypeOf pActiveView Is IPageLayout Then
        
        'And assign ResampleRatio to the Maps in the PageLayout
        Dim pGraphicsContainer As IGraphicsContainer
        Set pGraphicsContainer = pActiveView
        pGraphicsContainer.Reset
        
        Dim pElement As IElement
        Set pElement = pGraphicsContainer.Next
        Do While Not pElement Is Nothing
            
            If TypeOf pElement Is IMapFrame Then
                Dim pMapFrame As IMapFrame
                Set pMapFrame = pElement
                Dim pTmpActiveView As IActiveView
                Set pTmpActiveView = pMapFrame.Map
                Set pOutputRasterSettings = _
                    pTmpActiveView.ScreenDisplay.DisplayTransformation
                pOutputRasterSettings.ResampleRatio = lOutputQuality
            End If
            DoEvents
            Set pElement = pGraphicsContainer.Next
        
        Loop
    End If
    
End Sub

Private Sub NewZip(sPath)
  'Create empty zip file
  If Len(Dir(sPath)) > 0 Then Kill sPath
  Open sPath For Output As #1
  Print #1, Chr$(80) & Chr$(75) & Chr$(5) & Chr$(6) & String(18, 0)
  Close #1
End Sub

