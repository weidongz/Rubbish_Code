package Min_Min;
import java.util.ArrayList;


import org.cloudbus.cloudsim.CloudletSchedulerTimeShared;
import org.cloudbus.cloudsim.Vm;;


/**
 * VmsCreator Creates VM Lists as per the User Requirements.
 * @author Linda J
 *
 */
public class VmsCreator {
	
	//vmlist creator function
	public ArrayList<Vm> createRequiredVms(int reqVms, int brokerId){
		
		ArrayList<Vm> vmlist = new ArrayList<Vm>();
		
    	//VM description
    	int vmid = 0;
    	//int mips = 1000;
//    	int[] mips={220, 200, 300, 450};
//    	long size = 1000; //image size (MB)
//    	int ram = 512; //vm memory (MB)
//    	long bw = 1000;
//    	int[] pesNumber = {1,2,1,1}; //number of cpus
//    	String vmm = "Xen"; //VMM name
    	long size = 10000; //image size (MB)
        int ram = 512; //vm memory (MB)
        int mips = 250;
        long bw = 1000;
        int pesNumber = 1; //number of cpus
        String vmm = "Xen"; //VMM name
    	
    	
    	for(vmid=0;vmid<reqVms;vmid++){
    		//add the VMs to the vmList
//    		vmlist.add(new Vm(vmid, brokerId, mips[vmid], pesNumber[vmid], ram, bw, 
    		vmlist.add(new Vm(vmid, brokerId, mips, pesNumber, ram, bw, 
    				size, vmm, new CloudletSchedulerTimeShared()));
    	}

    	System.out.println("VmsCreator function Executed... SUCCESS:)");
		return vmlist;
		
	}

}
