package Min_Min;


import java.util.ArrayList;

import org.cloudbus.cloudsim.Cloudlet;
import org.cloudbus.cloudsim.DatacenterBroker;
import org.cloudbus.cloudsim.Vm;

/**
 * A Broker that schedules Tasks to the VMs 
 * as per FCFS Scheduling Policy
 * @author Linda J
 *
 */
public class MinminBroker extends DatacenterBroker {

	public MinminBroker(String name) throws Exception {
		super(name);
		// TODO Auto-generated constructor stub
	}

	//scheduling function
	
	
	public void scheduleTaskstoVms(){
		int reqTasks= cloudletList.size();
		int reqVms= vmList.size();
		//int k=0;
		
		ArrayList<Cloudlet> clist = new ArrayList<Cloudlet>();
		ArrayList<Vm> vlist = new ArrayList<Vm>();
		
		for (Cloudlet cloudlet : getCloudletList()) {
    		clist.add(cloudlet);
    		//System.out.println("clist:" +clist.get(k).getCloudletId());
    		//k++;
		}
		//k=0;
		for (Vm vm : getVmList()) {
    		vlist.add(vm);
    		//System.out.println("vlist:" +vlist.get(k).getId());
    		//k++;
		}

		
		double completionTime[][] = new double[reqTasks][reqVms];
		double execTime[][] = new double[reqTasks][reqVms];
		double time =0.0;
		
		for(int i=0; i<reqTasks; i++){
			for(int j=0; j<reqVms; j++){
				time = getCompletionTime(clist.get(i), vlist.get(j));
				completionTime[i][j]= time;
				time = getExecTime(clist.get(i), vlist.get(j));
				execTime[i][j]= time;
				
				System.out.print(execTime[i][j]+" ");
				
			}
			System.out.println();
			
		}
		
		int minCloudlet=0;
		int minVm=0;
		double min=-1.0d;
		
		for(int c=0; c< clist.size(); c++){
			
			for(int i=0;i<clist.size();i++){
				for(int j=0;j<(vlist.size()-1);j++){
					if(completionTime[i][j+1] > completionTime[i][j] && completionTime[i][j+1] > 0.0){
						minCloudlet=i;
					}
				}
			}
			
			
				for(int j=0; j<vlist.size(); j++){
					time = getExecTime(clist.get(minCloudlet), vlist.get(j));
					if(j==0){
						min=time;
					}
					if(time < min && time > -1.0){
						minVm=j;
						min=time;
					}
				
			}
			
			bindCloudletToVm(minCloudlet, minVm);
			clist.remove(minCloudlet);
			
			for(int i=0; i<vlist.size(); i++){
				completionTime[minCloudlet][i]=-1.0;
			}
			
		}
		
		
	}	
	
	
	private double getCompletionTime(Cloudlet cloudlet, Vm vm){
		double waitingTime = cloudlet.getWaitingTime();
		double execTime = cloudlet.getCloudletLength() / (vm.getMips()*vm.getNumberOfPes());
		
		double completionTime = execTime + waitingTime;
		
		return completionTime;
	}
	
	private double getExecTime(Cloudlet cloudlet, Vm vm){
		return cloudlet.getCloudletLength() / (vm.getMips()*vm.getNumberOfPes());
	}
}
