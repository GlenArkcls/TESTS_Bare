Function Echo-WithColour
{
    [CmdletBinding()]
    param
    (
        [Parameter(Mandatory=$true,ValueFromPipeline=$true)]
        [AllowEmptyString()]
        [string]
        $line
    )
    BEGIN{
     $v="beginning"
     Out-Host $v
    }
    PROCESS
    {
   
    if($line.IndexOf("ok") -ne -1)
    {
        $ix=$line.IndexOf("ok")
        $pre=$line.Substring(0,$ix)
        $post=""
        if($ix+2 -lt $line.Length-1)
        {
            $post=$line.Substring($ix+2)
        }
       Write-Host $pre -NoNewLine
        Write-Host "ok" -ForegroundColor Green -NoNewLine
        Write-Host $post

    }
    elseif($line.IndexOf("FAIL") -ne -1)
    {
        $ix=$line.IndexOf("FAIL")
        $pre=$line.Substring(0,$ix)
        $post=""
        if($ix+4 -lt $line.Length-1)
        {
            $post=$line.Substring($ix+4)
        }
        Write-Host $pre -NoNewLine
        Write-Host "FAIL" -ForegroundColor RED -NoNewLine
        Write-Host $post
    }
    else
    {
        Write-Host $line
    }
    }
    
    END{}


}