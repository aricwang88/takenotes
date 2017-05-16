# takenotes
My notes
#Erlang trace

/* erlang trace

1). Login to erlang shell on ANCB as root;

 >erl
 
2). Run the command below in erlang shell: 

 trace:start([{return,on},{caller,on},{local,on},{modvar,off},{protect,on}]). 
 
trace:start([{return,on},{caller,on},{local,on},{circular,off},{mode,full}]).


trace:activate(["pdp_restoration_apn","pdp_deactivation_controller_main","ssuses_deactivation_it","iterator_agent_helper"]). 

 3). Stop and collect Erlang trace. Commands to be executed in erlang shell on NCB (as root) as below: 
 
 trace:stop(). 
 
 trace:merge([fast,pretty]). 
 
 4). Then please send the erlang tracing resulting file: /tmp/DPE_LOG/Erlang_trace_merged.log 
 


