import sys
import os
import re # Regular Expressions
import json

# Set up globals 
Prog = ""
Verb = ""
Pipe = ""
outfile = 0
EchoString = ""
ParmPass = 0

########################################################################
def WriteProlog():

      global Prog, Verb, Pipe, outfile, EchoString
      
      if Prog == "Sim":
         outfile.write("#include \"42.h\"\n\n")
      elif Prog == "App":
         outfile.write("#include \"Ac.h\"\n\n")
      #endif
      
      if Pipe == "Gmsec":
         outfile.write("#include \"gmseckit.h\"\n")
      #endif

      outfile.write("/**********************************************************************/\n")
      
      if Pipe == "Socket":
         if Prog == "Sim":
            outfile.write("void WriteToSocket(SOCKET Socket)\n")
         else:
            outfile.write("void WriteToSocket(SOCKET Socket, struct AcType *AC)\n")
         #endif
      elif Pipe == "Gmsec":
         if Prog == "Sim":
            outfile.write("void WriteToGmsec(GMSEC_ConnectionMgr ConnMgr,GMSEC_Status status)\n")
         else:
            outfile.write("void WriteToGmsec(GMSEC_ConnectionMgr ConnMgr,GMSEC_Status status,struct AcType *AC)\n")
         #endif
      elif Pipe == "File":
         if Prog == "Sim":
            outfile.write("void WriteToFile(FILE *StateFile)\n")
         else:
            outfile.write("void WriteToFile(FILE *StateFile, struct AcType *AC)\n")
         #endif
      #endif
      
      outfile.write("{\n\n")
      outfile.write("      long Isc,Iorb,Iw,i;\n")
      
      if Pipe == "Socket":
         outfile.write("      int Success;\n")
         outfile.write("      char AckMsg[5] = \"Ack\\n\";\n")
         outfile.write("      char Msg[16384];\n")
         outfile.write("      long MsgLen = 0;\n")
         outfile.write("      long LineLen;\n")
      elif Pipe == "Gmsec":
         outfile.write("      char Header[40] = \"GMSEC.42.TX.MSG.LOG\";\n")
         outfile.write("      GMSEC_Message AckMsg;\n")
         outfile.write("      char Msg[16384];\n")
         outfile.write("      long MsgLen = 0;\n")
         outfile.write("      long LineLen;\n")
      #endif
      outfile.write("      char line[512];\n\n")

      if Prog == "App":
         outfile.write("      Isc = AC->ID;\n\n")
      #endif
      
      if Prog == "Sim":
         outfile.write("      sprintf(line,\"TIME %ld-%03ld-%02ld:%02ld:%012.9lf\\n\",\n")
         outfile.write("         Year,doy,Hour,Minute,Second);\n")
         if Pipe == "Socket":
            outfile.write("      LineLen = strlen(line);\n")
            outfile.write("      memcpy(&Msg[MsgLen],line,LineLen);\n")
            outfile.write("      MsgLen += LineLen;\n")
         elif Pipe == "Gmsec":
            outfile.write("      LineLen = strlen(line);\n")
            outfile.write("      memcpy(&Msg[MsgLen],line,LineLen);\n")
            outfile.write("      MsgLen += LineLen;\n")
         elif Pipe == "File":
            outfile.write("      fprintf(StateFile,\"%s\",line);\n")
         #endif
         outfile.write("      if ("+EchoString+") printf(\"%s\",line);\n\n")
      #endif
      
 
########################################################################
def ReadProlog():

      global Prog, Verb, Pipe, outfile, EchoString

      if Prog == "Sim":
         outfile.write("#include \"42.h\"\n\n")
      elif Prog == "App":
         outfile.write("#include \"Ac.h\"\n\n")
      #endif

      if Pipe == "Gmsec":
         outfile.write("#include \"gmseckit.h\"\n")
      #endif

      outfile.write("/**********************************************************************/\n")
      
      if Pipe == "Socket":
         if Prog == "Sim":
            outfile.write("void ReadFromSocket(SOCKET Socket)\n")
         else:
            outfile.write("void ReadFromSocket(SOCKET Socket, struct AcType *AC)\n")
         #endif
      elif Pipe == "Gmsec":
         if Prog == "Sim":
            outfile.write("void ReadFromGmsec(GMSEC_ConnectionMgr ConnMgr,GMSEC_Status status)\n")
         else:
            outfile.write("void ReadFromGmsec(GMSEC_ConnectionMgr ConnMgr,GMSEC_Status status,struct AcType *AC)\n")
      elif Pipe == "File":
         if Prog == "Sim":
            outfile.write("void ReadFromFile(FILE *StateFile)\n")
         else:
            outfile.write("void ReadFromFile(FILE *StateFile, struct AcType *AC)\n")
         #endif
      elif Pipe == "Cmd":
         outfile.write("void ReadFromCmd(void)\n");
      #endif
      
      outfile.write("{\n\n")
      outfile.write("      struct SCType *S;\n")
      outfile.write("      struct OrbitType *O;\n")
      outfile.write("      struct DynType *D;\n")
      outfile.write("      long Isc,Iorb,Iw,i;\n")
      outfile.write("      char line[512] = \"Blank\";\n")
      outfile.write("      long RequestTimeRefresh = 0;\n")
      outfile.write("      long Done;\n")
      if Pipe == "Gmsec":
         outfile.write("      char Msg[16384];\n")
         outfile.write("      GMSEC_Message GsMsg;\n")
         outfile.write("      GMSEC_Field Field;\n")
         outfile.write("      char AckMsg[5] = \"Ack\\n\";\n")
         outfile.write("      long Imsg,Iline;\n")
      elif Pipe == "Socket":
         outfile.write("      char Msg[16384];\n")
         outfile.write("      char AckMsg[5] = \"Ack\\n\";\n")
         outfile.write("      long Imsg,Iline;\n")
      #endif
      outfile.write("      double DbleVal[30];\n")
      outfile.write("      long LongVal[30];\n\n")
      if Prog == "App":
         outfile.write("      long Year,doy,Month,Day,Hour,Minute;\n")
         outfile.write("      double Second;\n")
      #endif
      
      if Pipe == "Socket":
         outfile.write("      long MsgLen;\n\n")
         outfile.write("      memset(Msg,'\\0',16384);\n")
         outfile.write("      MsgLen = 0;\n")
         outfile.write("      recv(Socket,Msg,16384,0);\n\n")
         outfile.write("      Done = 0;\n")
         outfile.write("      Imsg = 0;\n")
         outfile.write("      while(!Done) {\n")
         outfile.write("         /* Parse lines from Msg, newline-delimited */\n")
         outfile.write("         Iline = 0;\n")
         outfile.write("         memset(line,'\\0',512);\n")
         outfile.write("         while(Msg[Imsg] != '\\n') {\n")
         outfile.write("            line[Iline++] = Msg[Imsg++];\n")
         outfile.write("         }\n")
         outfile.write("         line[Iline++] = Msg[Imsg++];\n")
      elif Pipe == "Gmsec":
         outfile.write("      GsMsg = connectionManagerReceive(ConnMgr,GMSEC_WAIT_FOREVER,status);\n")
         outfile.write("      CheckGmsecStatus(status);\n")
         outfile.write("      Field = messageGetField(GsMsg,\"MSG-TEXT\",status);\n")
         outfile.write("      CheckGmsecStatus(status);\n")
         outfile.write("      strcpy(Msg,stringFieldGetValue(Field,status));\n")
         outfile.write("      CheckGmsecStatus(status);\n\n")
         outfile.write("      Done = 0;\n")
         outfile.write("      Imsg = 0;\n")
         outfile.write("      while(!Done) {\n")
         outfile.write("         /* Parse lines from Msg, newline-delimited */\n")
         outfile.write("         Iline = 0;\n")
         outfile.write("         memset(line,'\\0',512);\n")
         outfile.write("         while(Msg[Imsg] != '\\n') {\n")
         outfile.write("            line[Iline++] = Msg[Imsg++];\n")
         outfile.write("         }\n")
         outfile.write("         line[Iline++] = Msg[Imsg++];\n")
      elif Pipe == "File":
         outfile.write("      Done = 0;\n")
         outfile.write("      while(!Done) {\n")
         outfile.write("         fgets(line,511,StateFile);\n")
      elif Pipe == "Cmd":
         outfile.write("      /* Placeholder */\n")
      #endif   
                 
      outfile.write("         if ("+EchoString+") printf(\"%s\",line);\n\n")

      outfile.write("         if (sscanf(line,\"TIME %ld-%ld-%ld:%ld:%lf\\n\",\n")
      outfile.write("            &Year,&doy,&Hour,&Minute,&Second) == 5)\n")
      outfile.write("            RequestTimeRefresh = 1;\n\n")

########################################################################
def WriteEpilog():

      global Prog, Verb, Pipe, outfile, EchoString

      outfile.write("      sprintf(line,\"[EOF]\\n\\n\");\n")
      outfile.write("      if ("+EchoString+") printf(\"%s\",line);\n\n")

      if Pipe == "Socket":
         outfile.write("      LineLen = strlen(line);\n")
         outfile.write("      memcpy(&Msg[MsgLen],line,LineLen);\n")
         outfile.write("      MsgLen += LineLen;\n")
         outfile.write("      Success = send(Socket,Msg,strlen(Msg),0);\n\n")
         outfile.write("      /* Wait for Ack */\n");
         outfile.write("      recv(Socket,AckMsg,5,0);\n")
      elif Pipe == "Gmsec":
         outfile.write("      LineLen = strlen(line);\n")
         outfile.write("      memcpy(&Msg[MsgLen],line,LineLen);\n")
         outfile.write("      MsgLen += LineLen;\n")
         outfile.write("      GmsecSend(Header,Msg,ConnMgr,status);\n")
         outfile.write("      /* Wait for ack */\n")
         outfile.write("      AckMsg = connectionManagerReceive(ConnMgr,GMSEC_WAIT_FOREVER,status);\n")
         outfile.write("      CheckGmsecStatus(status);\n")
         outfile.write("      messageDestroy(&AckMsg);\n")
      elif Pipe == "File":
         outfile.write("      fprintf(StateFile,\"%s\",line);\n")
      #endif
      outfile.write("}\n")
      
########################################################################
def ReadEpilog():

      global Prog, Verb, Pipe, outfile

      outfile.write("\n")
      outfile.write("         if (!strncmp(line,\"[EOF]\",5)) {\n")
      outfile.write("            Done = 1;\n")
      outfile.write("            sprintf(line,\"[EOF] reached\\n\");\n")
      outfile.write("         }\n")
      
      if Pipe == "Socket":
         outfile.write("         if (Imsg > 16383) {\n")
         outfile.write("            Done = 1;\n")
         outfile.write("            printf(\"Imsg limit exceeded\\n\");\n")
         outfile.write("         }\n")
         outfile.write("      }\n\n")
         outfile.write("      /* Acknowledge receipt */\n")
         outfile.write("      send(Socket,AckMsg,strlen(AckMsg),0);\n\n")
      elif Pipe == "Gmsec":
         outfile.write("         messageDestroy(&GsMsg);\n")
         outfile.write("      }\n\n")
      
         outfile.write("      /* Acknowledge receipt */\n")
         outfile.write("      GmsecSend(\"GMSEC.42.RX.MSG.LOG\",AckMsg,ConnMgr,status);\n\n")
      elif Pipe == "File":
         outfile.write("      }\n\n")
      elif Pipe == "Cmd":
         outfile.write("      }\n\n")
      #endif
      
########################################################################
def TimeRefreshCode():

      global outfile,Prog
      
      if Prog == "Sim":
         outfile.write("      if (RequestTimeRefresh) {\n")
         outfile.write("         /* Update AbsTime, SimTime, etc */\n")
         outfile.write("         DOY2MD(Year,doy,&Month,&Day);\n")
         outfile.write("         AbsTime = DateToAbsTime(Year,Month,Day,Hour,Minute,Second);\n")
         outfile.write("         JulDay = AbsTimeToJD(AbsTime);\n")
         outfile.write("         JDToGpsTime(JulDay,&GpsRollover,&GpsWeek,&GpsSecond);\n")
         outfile.write("         SimTime = AbsTime-AbsTime0;\n")
         outfile.write("      }\n\n")
      else:
         outfile.write("      if (RequestTimeRefresh) {\n")
         outfile.write("         /* Update AC->Time */\n")
         outfile.write("         DOY2MD(Year,doy,&Month,&Day);\n")
         outfile.write("         AC->Time = DateToAbsTime(Year,Month,Day,Hour,Minute,Second);\n")
         outfile.write("      }\n\n")
      #endif
            
########################################################################
def StateRefreshCode():

      global outfile
      
      outfile.write("\n/* .. Refresh SC states that depend on inputs */\n\n")

      outfile.write("      for(Isc=0;Isc<Nsc;Isc++) {\n")
      outfile.write("         if (SC[Isc].RequestStateRefresh) {\n")
      outfile.write("            S = &SC[Isc];\n")
      outfile.write("            S->RequestStateRefresh = 0;\n")
      outfile.write("            if (S->Exists) {\n")
      outfile.write("               /* Update  RefOrb */\n")
      outfile.write("               O = &Orb[S->RefOrb];\n")
      outfile.write("               O->Epoch = AbsTime;\n")
      outfile.write("               for(i=0;i<3;i++) {\n")
      outfile.write("                  S->PosN[i] = O->PosN[i] + S->PosR[i];\n")
      outfile.write("                  S->VelN[i] = O->VelN[i] + S->VelR[i];\n")
      outfile.write("               }\n")
      outfile.write("               RV2Eph(O->Epoch,O->mu,O->PosN,O->VelN,\n")
      outfile.write("                  &O->SMA,&O->ecc,&O->inc,&O->RAAN,\n")
      outfile.write("                  &O->ArgP,&O->anom,&O->tp,\n")
      outfile.write("                  &O->SLR,&O->alpha,&O->rmin,\n")
      outfile.write("                  &O->MeanMotion,&O->Period);\n")
      outfile.write("               FindCLN(O->PosN,O->VelN,O->CLN,O->wln);\n\n")

      outfile.write("               /* Update Dyn */\n")
      outfile.write("               MapJointStatesToStateVector(S);\n")
      outfile.write("               D = &S->Dyn;\n")
      outfile.write("               MapStateVectorToBodyStates(D->u,D->x,D->uf,D->xf,S);\n")
      outfile.write("               MotionConstraints(S);\n")
      outfile.write("            }\n")
      outfile.write("         }\n")
      outfile.write("      }\n")

########################################################################
def WriteCodeBlock(Indent,FmtPrefix,ArrayIdx,ArgPrefix,VarString,IdxLen,Ni,Nj,StructIdxString,FormatString):

      global Prog, Verb, Pipe, outfile, EchoString

      line = Indent+"   sprintf(line,\""
      line += FmtPrefix
      line += VarString
      line += " ="
      for i in range (0,Ni):
         for j in range (0,Nj):
            line += " "+FormatString
         #next j
      #next i
      line += "\\n\",\n"+"      "+Indent+ArrayIdx+StructIdxString
      if Nj > 1:
         for i in range (0,Ni):
            for j in range (0,Nj):
               line += ",\n"+"      "+Indent+ArgPrefix+VarString+"["+str(i)+"]["+str(j)+"]"
            #next j
         #next i
      elif Ni > 1:
         for i in range (0,Ni):
            line += ",\n"+"      "+Indent+ArgPrefix+VarString+"["+str(i)+"]"
         #next i
      else:
         line += ",\n"+"      "+Indent+ArgPrefix+VarString
      #endif
      
      line += ");\n"

      outfile.write(line)
      outfile.write("   "+Indent+"if ("+EchoString+") printf(\"%s\",line);\n")
      if Pipe == "Socket":
         outfile.write("   "+Indent+"LineLen = strlen(line);\n")
         outfile.write("   "+Indent+"memcpy(&Msg[MsgLen],line,LineLen);\n")
         outfile.write("   "+Indent+"MsgLen += LineLen;\n\n")
      elif Pipe == "Gmsec":
         outfile.write("   "+Indent+"LineLen = strlen(line);\n")
         outfile.write("   "+Indent+"memcpy(&Msg[MsgLen],line,LineLen);\n")
         outfile.write("   "+Indent+"MsgLen += LineLen;\n\n")
      elif Pipe == "File":
         outfile.write("   "+Indent+"fprintf(StateFile,\"%s\",line);\n\n")
      #endif

########################################################################
def ReadCodeBlock(Indent,FmtPrefix,ArrayIdx,ArgPrefix,ArgString,VarString,IdxLen,Ni,Nj,StructIdxString,Narg,FormatString):

      global Prog, outfile

      line = Indent+"if (sscanf(line,\""
      line += FmtPrefix
      line += VarString
      line += " ="
      for i in range (0,Ni):
         for j in range (0,Nj):
            line += " "+FormatString
         #next j
      #next i
      line += "\","+"\n   "+Indent+"&"+ArrayIdx+StructIdxString
      if Nj > 1:
         for i in range (0,Ni):
            for j in range (0,Nj):
               line += ","+"\n   "+Indent+"&"+ArgString+"["+str(Nj*i+j)+"]"
            #next j
         #next i
      elif Ni > 1:
         for i in range (0,Ni):
            line += ","+"\n   "+Indent+"&"+ArgString+"["+str(i)+"]"
         #next i
      else:
         line += ","+"\n   "+Indent+"&"+ArgString+"[0]"
      #endif
      line += ") == "+str(Narg)+") {"
      
      if Prog == "App":
         line += "\n   "+Indent+"if (Isc == AC->ID) {"
         Indent += "   "
      #endif
      
      if Nj > 1:
         for i in range (0,Ni):
            for j in range (0,Nj):
               line += "\n   "+Indent+ArgPrefix+VarString+"["+str(i)+"]["+str(j)+"] = "+ArgString+"["+str(Nj*i+j)+"];"
            #next j
         #next i
      elif Ni > 1:
         for i in range (0,Ni):
            line += "\n   "+Indent+ArgPrefix+VarString+"["+str(i)+"] = "+ArgString+"["+str(i)+"];"
         #next i
      else:
         line += "\n   "+Indent+ArgPrefix+VarString+" = "+ArgString+"[0];"
      #endif
      if Prog == "App":
         Indent = Indent[0:-3]
         line += "\n   "+Indent+"}"
      #endif
      if ArgPrefix.startswith("SC") and ArgPrefix.count("AC") == 0:
         line += "\n   "+Indent+"SC[Isc].RequestStateRefresh = 1;"
      #endif
      line += "\n"+Indent+"}\n\n"

      outfile.write(line)

########################################################################
def ParseStruct(StructList,Struct,Indent,FmtPrefix,ArrayIdx,ArgPrefix,StructIdxString,Narg):

      global Prog, Verb, Pipe, outfile, ParmPass

      Primitives = {"long","double"}

      VarList = Struct["Table Data"]
      for Var in VarList:
         DataType = Var["Data Type"]
         if DataType in Primitives:
            VarString = Var["Variable Name"]
            if "Array Size" in Var:
               IdxString = Var["Array Size"].strip(r"[]")
               IdxList =  IdxString.split(",")
               IdxLen = len(IdxList)
               if IdxLen == 2:
                  Ni = int(IdxList[0])
                  Nj = int(IdxList[1])
               elif IdxList[0].isnumeric():
                  Ni = int(IdxList[0])
                  Nj = 1
               else: 
                  Ni = 1
                  Nj = 1
               #endif
            else:
               IdxLen = 0
               Ni = 1
               Nj = 1
            #endif
            if DataType == "long":
               WriteFormatString = "%ld"
               ReadFormatString = "%ld"
               ArgString = "LongVal"
            else:
               WriteFormatString = "%18.12le"
               ReadFormatString = "%le"
               ArgString = "DbleVal"
            #endif            
            if Prog == "Sim":
               ReadWrite = Var["Sim Read/Write"]
            elif Prog == "App":
               ReadWrite = Var["App Read/Write"]
            else:
               ReadWrite = ""
            #endif
            PktRole = Var["Packet Role"]
            if ParmPass == 1:
               if Verb == "WriteTo" and PktRole == "PRM" and ReadWrite == "":
                  WriteCodeBlock(Indent,FmtPrefix,ArrayIdx,ArgPrefix,VarString,IdxLen,Ni,Nj,StructIdxString,WriteFormatString)
               #endif
               if Verb == "ReadFrom" and PktRole == "PRM" and ReadWrite == "":
                  ReadCodeBlock(Indent,FmtPrefix,ArrayIdx,ArgPrefix,ArgString,VarString,IdxLen,Ni,Nj,StructIdxString,Narg+Ni*Nj,ReadFormatString)
               #endif
            else:
               if Verb == "WriteTo" and ReadWrite in ["WRITE","READ_WRITE"]:
                  WriteCodeBlock(Indent,FmtPrefix,ArrayIdx,ArgPrefix,VarString,IdxLen,Ni,Nj,StructIdxString,WriteFormatString)
               #endif
               if Verb == "ReadFrom" and ReadWrite in ["READ","READ_WRITE"]:
                  ReadCodeBlock(Indent,FmtPrefix,ArrayIdx,ArgPrefix,ArgString,VarString,IdxLen,Ni,Nj,StructIdxString,Narg+Ni*Nj,ReadFormatString)
               #endif
               if Prog == "Sim" and Verb == "ReadFrom" and Pipe == "Cmd" and Var["Cmd Read"] == "READ":
                  ReadCodeBlock(Indent,FmtPrefix,ArrayIdx,ArgPrefix,ArgString,VarString,IdxLen,Ni,Nj,StructIdxString,Narg+Ni*Nj,ReadFormatString)
               #endif
            #endif
         else: # struct
            for SubStruct in StructList:
               if SubStruct["Table Name"] == Var["Data Type"]:
                  LocalFmtPrefix = FmtPrefix + Var["Variable Name"]
                  LocalArgPrefix = ArgPrefix + Var["Variable Name"]
                  LocalStructIdxString = StructIdxString
                  if "Array Size" in Var:
                     IdxString = Var["Array Size"].strip(r"[]")
                     IdxList =  IdxString.split(",")
                     IdxLen = len(IdxList)
                     if IdxString.isalpha():
                        if Verb == "WriteTo":
                           outfile.write(Indent+"   for(i=0;i<"+ArgPrefix+IdxString+";i++) {\n")
                           LocalIndent = Indent+"   "
                           if Prog == "Sim":
                              LocalStructIdxString += ",i"
                           else:
                              LocalStructIdxString += ",i"
                           #endif
                        else:
                           LocalIndent = Indent
                           LocalStructIdxString += ",&i"
                        #endif
                        LocalFmtPrefix += "[%ld]."
                        LocalArgPrefix += "[i]."
                        LocalNarg = Narg+1
                        ParseStruct(StructList,SubStruct,LocalIndent,LocalFmtPrefix,ArrayIdx,LocalArgPrefix,LocalStructIdxString,LocalNarg)
                        if Verb == "WriteTo":
                           outfile.write(Indent+"   }\n\n")
                        #endif
                     elif IdxLen == 2:
                        LocalFmtPrefix += "[%ld][%ld]."
                        LocalArgPrefix += "[i][j]."
                        if Verb == "WriteTo":
                           LocalStructIdxString += ",i,j"
                        else:
                           LocalStructIdxString += ",&i,&j"
                        #endif
                        LocalNarg = Narg+2
                        LocalIndent = Indent+""
                        ParseStruct(StructList,SubStruct,LocalIndent,LocalFmtPrefix,ArrayIdx,LocalArgPrefix,LocalStructIdxString,LocalNarg)
                     else:
                        LocalFmtPrefix += "[%ld]."
                        LocalArgPrefix += "[i]."
                        if Verb == "WriteTo":
                           LocalStructIdxString += ",i"
                        else:
                           LocalStructIdxString += ",&i"
                        #endif
                        LocalNarg = Narg+1
                        LocalIndent = Indent+""
                        ParseStruct(StructList,SubStruct,LocalIndent,LocalFmtPrefix,ArrayIdx,LocalArgPrefix,LocalStructIdxString,LocalNarg)
                     #endif
                  else:
                     LocalFmtPrefix += "."
                     LocalArgPrefix += "."
                     LocalIndent = Indent+""
                     ParseStruct(StructList,SubStruct,LocalIndent,LocalFmtPrefix,ArrayIdx,LocalArgPrefix,LocalStructIdxString,Narg)
                  #endif
               #endif
            #next SubStruct
         #endif           
      #next Var
########################################################################
def StripEmptyLoops(infile,outfile):

      line1 = infile.readline()
      
      while (line1 != ''):  # EOF
         StrippedLine1 = line1.strip()
         FoundFor = 0
         LoopIsEmpty = 0
         if StrippedLine1.startswith('for'):
            FoundFor = 1
            line2 = infile.readline()
            StrippedLine2 = line2.strip()
            if StrippedLine2.startswith('}'):
               LoopIsEmpty = 1
               line3 = infile.readline() # Blank line
            #endif
         #endif

         if (FoundFor and LoopIsEmpty):
            pass
            # Write nothing
         elif FoundFor:
            outfile.write(line1)
            outfile.write(line2)
         else:
            outfile.write(line1)
         #endif   
      
         line1 = infile.readline()
      #end while
            
########################################################################
def main():

      global Prog, Verb, Pipe, outfile, EchoString, ParmPass
      
      ProgList = {"Sim","App"}
      VerbList = {"WriteTo","ReadFrom"}
      PipeList = {"Socket","Gmsec","File","Cmd"}
      
      infile = open('42.json','rU')
      StructDict = json.load(infile)
      infile.close()
      
      for Prog in ProgList:
      
         if Prog == "Sim":
            EchoString = "EchoEnabled"
         else:
            EchoString = "AC->EchoEnabled"
         #endif
         
         for Verb in VerbList:
            for Pipe in PipeList:
            
               if not(Verb == "WriteTo" and Pipe == "Cmd") and not (Prog == "App" and Pipe == "Gmsec"):
            
                  outfile = open("TempIpc.c","w")      
            
                  if Verb == "WriteTo":
                     WriteProlog()
                  elif Verb == "ReadFrom":
                     ReadProlog()
                  #endif
               
                  for ParmPass in [0,1]:
               
                     StructList = StructDict["Table Definition"] 
                     for Struct in StructList:

                        Indent = "      "
            
                        if Prog == "Sim":
                  
                           if Struct["Table Name"] == "SCType":
                              if ParmPass == 0:
                                 if Verb == "WriteTo":
                                    outfile.write(Indent+"for(Isc=0;Isc<Nsc;Isc++) {\n")
                                    outfile.write(Indent+"   if (SC[Isc].Exists) {\n")
                                 #endif
                                 ParseStruct(StructList,Struct,Indent+"   ","SC[%ld].","Isc","SC[Isc].","",1) 
                                 if Verb == "WriteTo":
                                    outfile.write(Indent+"   }\n")
                                    outfile.write(Indent+"}\n\n")
                                 #endif
                              #endif
                           #endif
                           if Struct["Table Name"] == "OrbitType":
                              if ParmPass == 0:
                                 if Verb == "WriteTo":
                                    outfile.write(Indent+"for(Iorb=0;Iorb<Norb;Iorb++) {\n")
                                    outfile.write(Indent+"   if (Orb[Iorb].Exists) {\n")
                                 #endif
                                 ParseStruct(StructList,Struct,Indent+"   ","Orb[%ld].","Iorb","Orb[Iorb].","",1) 
                                 if Verb == "WriteTo":
                                    outfile.write(Indent+"   }\n")
                                    outfile.write(Indent+"}\n\n")
                                 #endif
                              #endif
                           #endif
                           if Struct["Table Name"] == "WorldType":
                              if ParmPass == 0:
                                 if Verb == "WriteTo":
                                    outfile.write(Indent+"for(Iw=1;Iw<NWORLD;Iw++) {\n")
                                    outfile.write(Indent+"   if (World[Iw].Exists) {\n")
                                 #endif
                                 ParseStruct(StructList,Struct,Indent+"   ","World[%ld].","Iw","World[Iw].","",1) 
                                 if Verb == "WriteTo":
                                    outfile.write(Indent+"   }\n")
                                    outfile.write(Indent+"}\n\n")
                                 #endif
                              #endif
                           #endif
                           if Struct["Table Name"] == "AcType":
                              if ParmPass == 1:
                                 if Verb == "WriteTo":
                                    Indent = "      "
                                    outfile.write(Indent+"for(Isc=0;Isc<Nsc;Isc++) {\n")
                                    outfile.write(Indent+"   if (SC[Isc].Exists) {\n")
                                    outfile.write(Indent+"      if (SC[Isc].AC.ParmLoadEnabled) {\n")
                                    #endif
                                 else:
                                    Indent = "         "
                                    outfile.write(Indent+"for(Isc=0;Isc<Nsc;Isc++) {\n")
                                    outfile.write(Indent+"   if (SC[Isc].Exists) {\n")
                                    outfile.write(Indent+"      if (SC[Isc].AC.ParmDumpEnabled) {\n")
                                    Indent += "   "
                                 #endif
                                 ParseStruct(StructList,Struct,Indent+"      ","SC[%ld].AC.","Isc","SC[Isc].AC.","",1) 
                                 if Verb == "WriteTo":
                                    outfile.write(Indent+"      }\n")
                                    outfile.write(Indent+"   }\n")
                                    outfile.write(Indent+"}\n\n")
                                 else:
                                    Indent = Indent[0:-3]
                                    outfile.write(Indent+"      }\n")
                                    outfile.write(Indent+"   }\n")
                                    outfile.write(Indent+"}\n\n")
                                 #endif
                              #endif
                           #endif
                        else:
                           if Struct["Table Name"] == "AcType":
                              if ParmPass == 1:
                                 if Verb == "WriteTo":
                                    Indent = "   "
                                    outfile.write(Indent+"   if (AC->ParmDumpEnabled) {\n")
                                    #endif
                                 else:
                                    Indent = "         "
                                    outfile.write(Indent+"if (AC->ParmLoadEnabled) {\n")
                                 #endif
                                 ParseStruct(StructList,Struct,Indent+"   ","SC[%ld].AC.","Isc","AC->","",1) 
                                 if Verb == "WriteTo":
                                    outfile.write(Indent+"   }\n\n")
                                 else:
                                    outfile.write(Indent+"}\n\n")
                                 #endif
                              else:
                                 if Verb == "WriteTo":
                                    Indent = "   "
                                    #endif
                                 else:
                                    Indent = "         "
                                 #endif
                                 ParseStruct(StructList,Struct,Indent,"SC[%ld].AC.","Isc","AC->","",1) 
                              #endif
                           #endif
                        #endif
                     #next Struct
                  #next ParmPass
               
                  if Verb == "WriteTo":
                     WriteEpilog() 
                  elif Verb == "ReadFrom":
                     ReadEpilog()
                     TimeRefreshCode()
                     if Prog == "Sim":
                        StateRefreshCode()
                     #endif
                     outfile.write("}\n")
                  #endif  
               
                  outfile.close()  
                  infile = open("TempIpc.c","rU")    
                  outfile = open("../Source/IPC/"+Prog+Verb+Pipe+".c","w")
                  StripEmptyLoops(infile,outfile)
                  infile.close()
                  outfile.close()
                  os.remove("TempIpc.c")      
                      
               #endif                
            #next Pipe
         #next Verb
      #next Prog
      
      
########################################################################
if __name__ == '__main__': main()
