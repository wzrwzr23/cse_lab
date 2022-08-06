from genericpath import exists
import sys
import threading
from copy import deepcopy

# Creating a reentrant lock for threads
bank_lock = threading.RLock()


class Banker:
    """
    A class to represent a banker.

    Attributes
    ----------
    number_of_customers (N) : int
        the number of customers
    number_of_resources (M) : int
        the number of resources
    available : list[int] (1 by M)
        the available amount of each resource
    max : list[list[int]] (N by M)
        the maximum demand of each customer
    allocation : list[list[int]] (N by M)
        the amount currently allocated
    need : list[list[int]] (N by M)
        the remaining needs of each customer

    Methods
    -------
    set_maximum_demand(customer_index, maximum_demand):
        Sets the maximum number of demand of each resource for a customer.

    print_state():
        Prints the current state of the bank.

    request_resources(customer_index, request):
        Requests resources for a customer loan.

    release_resources(customer_index, release):
        Releases resources borrowed by a customer. Assume release is valid for simplicity.

    check_safe(customer_index, request):
        Checks if the request will leave the bank in a safe state.

    @staticmethod
    run_file(filename):
        Parses and runs the file simulating a series of resource request and releases.
    """

    def __init__(
        self, available_resources, number_of_customers, number_of_resources
    ):
        """
        Constructor for the Banker class.

        Parameters
        ----------
            resources : list[int]
                an array of the available count for each resource
            number_of_customers : int
                the number of customers
        """
        # Set the number of resources
        self.number_of_resources = number_of_resources
        self.M = self.number_of_resources  # to be coherent with notes

        # Set the number of customers
        self.number_of_customers = number_of_customers
        self.N = self.number_of_customers  # to be coherent with notes

        # Set the value of bank resources to available
        self.available = available_resources

        # Set the array size for maximum, allocation, and need
        self.max = [
            [0 for _ in range(self.number_of_resources)]
            for _ in range(self.number_of_customers)
        ]
        self.allocation = [
            [0 for _ in range(self.number_of_resources)]
            for _ in range(self.number_of_customers)
        ]
        self.need = [
            [0 for _ in range(self.number_of_resources)]
            for _ in range(self.number_of_customers)
        ]

    def set_maximum_demand(self, customer_index, maximum_demand):
        """
        Sets the maximum number of demand of each resource for a customer.

        Parameters
        ----------
        customer_index : int
            the customer's index (0-indexed)
        maximum_demand : list[int]
            an array of the maximum demanded count for each resource

        Returns
        -------
        None
        """
        # Add customer, update maximum and need
        for idx, val in enumerate(maximum_demand):
            self.max[customer_index][idx] = val
            self.need[customer_index][idx] = val

    def request_resources(self, customer_index, request):
        """
        Request resources for a customer loan.

        Parameters
        ----------
        customer_index : int
            the customer's index (0-indexed)
        request : list[int]
            an array of the requested count for each resource

        Returns
        -------
        True : if the requested resources can be loaned
        False : otherwise
        """

        bank_lock.acquire()
        # Print the request
        print(f"Customer {customer_index} requesting\n{request}")
        for idx, req_val in enumerate(request):
            # Check if request is larger than need
            if self.need[customer_index][idx] < req_val:
                return False
            # Check if request is larger than available
            if self.available[idx] < req_val:
                return False

        # Task 1
        # TODO: Check if the state is safe or not by calling check_safe, right now it is hardcoded to True
        # 1. Perform a deepcopy of available, need, and allocation
        # 2. Call the check_safe method with new data in (1)
        # 3. Store the return value of (2) in variable safe
        # DO NOT PRINT ANYTHING ELSE

        ### BEGIN ANSWER HERE ###
        work = deepcopy(self.available)
        need_copy = deepcopy(self.need)
        allocation_copy = deepcopy(self.allocation)
        safe = self.check_safe(customer_index, request, work, need_copy, allocation_copy)  # Change this line


        ### END OF TASK 1 ###

        if safe:
            # If it is safe, allocate the resources to customer customer_number
            for idx, req_val in enumerate(request):
                self.allocation[customer_index][idx] += req_val
                self.need[customer_index][idx] -= req_val
                self.available[idx] -= req_val

            bank_lock.release()
            return True
        else:
            bank_lock.release()
            return False

    def release_resources(self, customer_index, release):
        """
        Releases resources borrowed by a customer. Assume the value of release is valid (will not release more than what's been allocated) for simplicity.

        Parameters
        ----------
        customer_index : int
            the customer's index (0-indexed)
        release : list[int]
            an array of the release count for each resource

        Returns
        -------
        None
        """
        print(f"Customer {customer_index} releasing\n{release}")

        bank_lock.acquire()
        # Release the resources from customer customer_number
        for idx, val in enumerate(release):
            self.allocation[customer_index][idx] -= val
            self.need[customer_index][idx] += val
            self.available[idx] += val
        bank_lock.release()

    def check_safe(self, customer_index, request, work, need, allocation):
        """
        Checks if the request will leave the bank in a safe state.

        Parameters
        ----------
        work, need, allocation : list[int], list[list[int]], list[list[int]]
            deep copy of available, need, and allocation matrices
        customer_index : int
            the customer's index (0-indexed)
        request : list[int]
            an array of the requested count for each resource

        Returns
        -------
        True : if the request resources will leave the bank in a safe state
        False : otherwise
        """
        bank_lock.acquire()

        # TASK 2
        # TODO: Check if the state is safe
        # 1. Create work list[int] of length self.M, set work = available
        # 2. Create finish list[int] of length self.N
        # 3. Find index i such that both finish[i] == False, need[i] <= work
        # 4. If such index in (3) exists, update work += allocation[i], finish[i] = True
        # 5. REPEAT step (3) until no such i exists
        # 6. If no such i exists anymore, and finish[i] == True for all i, set safe = True
        # 7. Otherwise, set safe = False
        # DO NOT PRINT ANYTHING ELSE

        ### BEGIN ANSWER HERE ###
        safe = False  # Change this line according to whether the request will be safe or not
        finish = [False]*self.N
        
        for i in range(self.M):
            work[i] = work[i] - request[i]
            need[customer_index][i] = need[customer_index][i] - request[i]
            allocation[customer_index][i] = allocation[customer_index][i] + request[i]
            
        exist = True
        while exist:
            exist = False
            for i in range(self.N):
                if finish[i]==False:
                    for j in range(self.M):
                        if need[i][j]<=work[j]:
                            check = True
                        else:
                            check = False
                            break
                    if check:
                        for j in range(self.M):
                            work[j]+=allocation[i][j]
                        finish[i]=True
                        exist = True
        
    
        # exist = True
        # while exist:
        #     exist = False
        #     idx=None
        #     for i in range(self.N):
        #         check = True
        #         for j in range(self.M):
        #             if need[i][j] > work[j] or finish[i]!=False:
        #                 check = False
        #                 break
        #         if check:
        #             idx = i
        #             break
        #     if idx!=None:
        #         for j in range(self.M):
        #             work[j] = work[j] + allocation[idx][j]
        #             finish[idx]=True    
        #             exist=True    

        for i in finish:
            if i ==False:
                safe= False
                break
            else:
                safe=True
       
        # for i in range(self.M):
        #     if request[i] <= work[i] and request[i] <= need[customer_index][i]:
        #         safe = True

        # if safe:
        #     for i in range(self.M):
        #         work[i] = work[i] - request[i]
        #         need[customer_index][i] = need[customer_index][i] - request[i]
        #         allocation[customer_index][i] = allocation[customer_index][i] + request[i]
        
            
            
        #     exist = True
        #     while exist:
        #         exist = False
        #         for i in range(self.N):
        #             update = True
        #             if finish[i] == False:
        #                 for j in range(self.M):

        #                     if need[i][j] > work[j]:
        #                         update = False
                                

        #                 if update:
        #                     finish[i]=True
        #                     exist = True
        #                     for j in range(self.M):
        #                         work[j] += allocation[i][j]
        


        # for i in range(self.N):
        #     if finish[i] == False:
        #         safe = False
        #         break
        #     else:
        #         safe = True

        ### END OF TASK 2 ###

        bank_lock.release()
        return safe

    def print_state(self):
        """
        Prints the current state of the bank.
        """
        # Print available
        print("\nCurrent state:")
        print("Available:")
        print(self.available)
        print()

        # Print maximum
        print("Maximum:")
        for i in self.max:
            print(i)
        print()

        # Print allocation
        print("Allocation:")
        for i in self.allocation:
            print(i)
        print()

        # Print need
        print("Need:")
        for i in self.need:
            print(i)
        print()

    @staticmethod
    def run_file(filename):
        """
        Parses and runs the file simulating a series of resource request and releases.
        Provided for your convenience.

        Parameters
        ----------
        filename : str
            the name of the file

        Returns
        -------
        None
        """
        try:
            with open(filename, "r") as fp:
                line_number = 1
                n = int(fp.readline().split(",")[1])

                line_number += 1
                m = int(fp.readline().split(",")[1])

                line_number += 1
                available_resources = [
                    int(i) for i in fp.readline().split(",")[1].split(" ")
                ]

                banker = Banker(available_resources, n, m)

                while True:
                    line_number += 1

                    line = next(fp)
                    tokens = line.strip().split(",")

                    match tokens[0]:
                        case "c":
                            banker.set_maximum_demand(
                                int(tokens[1]),
                                [int(i) for i in tokens[2].split(" ")],
                            )
                        case "r":
                            banker.request_resources(
                                int(tokens[1]),
                                [int(i) for i in tokens[2].split(" ")],
                            )
                        case "f":
                            banker.release_resources(
                                int(tokens[1]),
                                [int(i) for i in tokens[2].split(" ")],
                            )
                        case "p":
                            banker.print_state()

        except StopIteration:
            return

        except FileNotFoundError:
            print(f"Error opening {filename}.")
            return

        except Exception as e:
            print(f"Error parsing resources on line {line_number}.")
            print(e)
            return


if __name__ == "__main__":
    # sys.argv[0] is the script name
    if len(sys.argv) > 1:
        Banker.run_file(sys.argv[1])
