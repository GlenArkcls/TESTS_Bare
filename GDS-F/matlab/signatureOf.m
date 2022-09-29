function sig = signatureOf(fnName)

    fndef=GetFunctionDefinition(fnName);
    for i=1:size(fndef.args,2)
        sig(i)=fndef.args{1,i}.type;
    end
end


       
     