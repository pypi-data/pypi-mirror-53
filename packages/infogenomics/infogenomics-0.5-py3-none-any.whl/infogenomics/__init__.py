import math
import numpy as np
import sys
import profile
import time


def get_kmers(s, k):

    """

        This function returns the set of k-mers that occur in a given string s
    --------
    Parameters:
        s (str) : the input string
        k (int) : the word length
    --------
    Returns:
        kmers : the set of k-mers
    """
    kmers = set()
    for i in range(len(s) - k +1):
        kmers.add(s[i:i+k])
    return kmers

def count_C(s, c):
    
    """

        This function returns the number of c in a given string s
    --------
    Parameters:
        s (str) : the input string
        c (str) : the character 
    --------    
    Returns:
        Count of c in s
    """    
    return s.count(c)

def count_occurrences(s, w):
    """
        Count the number of occurences of w in s
        --------
        Parameters:
            s (str)
            w (str)
        --------
        Returns:
            count of w in s.
    """
    count = 0
    for i in range(len(s)-len(w) +1):
        if s[i:i+len(w)] == w:
            count += 1
    return count

def h_r_d(s, k):
    """

        This function prints the kmers and if it's an hapax, a repeat, or a duplex
    -------
    Parameters:
        s (str) : the input string
        k (int) : the length of the kmer
    -------
    Returns:
        void
    """
    kmers = get_kmers(s,k)
    for kmer in kmers:
        m = count_occurrences(s,kmer)
        if m == 1:
            print(kmer + " is an hapax")
        else:
            print(kmer + " is a repeat")
        if m == 2:
            print(kmer + " is a duplex")
            

def list_words_2(prefix, k, nuc_alphabet, words):
    """ 
        This function computes all the  words of an alphabet with length k and a prefix. 
        Example : prefix = 'a', k = 2,  nuc_alphabet = ['a', 'c', 'g', 't'], words = set() 
        list_words_2(prefix, k , nuc_alphabet, words) -->  {'ac', 'at', 'ag', 'aa'}
    -------
    Parameters:
        prefix (str) : prefix 
        k (int) : the length of kmer
        nuc_alpabet (list()) : the alphabet
        words set() : the set of words.
    -------
    Returns:
        void
    """
    if len(prefix) == k:
        words.add(prefix)
    else:
        for a in nuc_alphabet:
            list_words_2(prefix + a, k, nuc_alphabet, words)        



def get_positions(s,w):
    """

        Return the starting postions in a reference string s where a word w occurs
    --------
    Paramters:
        s (str) : the reference string
        w (str) : the searched word
    --------
    Returns:
        list[int] : the positions
    """
    positions = list()
    for i in range(len(s)):
        if s[i:i+len(w)] == w:
            positions.append(i)
    return positions


def mrl(s):
    """

        Calculate the maximal repeat length of a string s
    --------
    Parameters:
        s (str) : the input string
    --------
    Returns: 
        mrl (int) : maximal repeat length
        kmer_mrl (str) : maximal repeat
        mult_mrl (int) : multeplicity
    """   
    k = 0
    mrl = 0
    kmer_mrl = ''
    mult_mrl = 0
    next_k = True
    while next_k:
        k += 1
        next_k = False
        for kmer in get_kmers(s,k):
            mult = count_occurrences(s,kmer)
            if mult > 1:
                mrl = k
                kmer_mrl = kmer
                mult_mrl = mult
                next_k = True
    return mrl, kmer_mrl, mult_mrl


def mhl(s):
    """

        Calculate the minimal hapax length of a string s 
    --------
    Parameters:
        s (str) : the input string
    --------
    Returns: 
        mhl () : minimal hapax length
        kmer_mrl (str) : maximal repeat
        mult_mrl (int) : multeplicity
    """
    k = 0
    mhl = 0
    kmer_mhl = ''
    mult_mhl = 0
    next_k = True
    while next_k:
        k += 1
        for kmer in get_kmers(s,k):
            mult = count_occurrences(s,kmer)
            if mult == 1:
                mhl = k
                kmer_mhl = kmer
                mult_mhl = mult
                next_k = False
    return mhl, kmer_mhl, mult_mhl


def get_alphabet(s):
    """
        This function returns the alphabet of a given string
    --------
    Parameters : 
        s (str) : the input string
    --------
    Returns:
        al (set()) : the alphabet 
    """
    al = set()
    for c in s:
        al.add(c)
    return al


def mfl(s, alphabet = None):
    """

        Calculate the minimal forbidden length of a string s 
        If alphabet is None ---> get_alphabet(s)
    --------
    Parameters:
        s (str) : the input string
    --------
    Returns:
        k (int) : minimal forbidden length of s
    """
    if alphabet == None:
        a = len(get_alphabet(s))
    else:
        a = len(alphabet)
        
    k = 0
    while True:
        k += 1
        kmers = get_kmers(s,k)
        if len(kmers) != a**k:
            return k   


def k_entropy(s,k):
    
    """

        Calculate the empirical entropy at word length k of a string s 
    --------
    Parameters:
        s (str) : the input string
        k (int) : the word length
    --------
    Returns:
        e (float) the empirical entropy
    """
    
    t = 0.0
    for kmer in get_kmers(s,k):
        t += count_occurrences(s,kmer)
    
    e = 0.0
    for kmer in get_kmers(s,k):
        e += math.log(count_occurrences(s,kmer) / t, 2)
    return -e
    

def get_multiplicity_distribution(s,k):
    """

        Return the word multiplciity distribution of k-mers occurrig in the string s
         ------
        Parameters:
            s (str) : the input string
            k (int) : the length of the k-mer 
        -------
        Returns:
            dict[str,int] : a dictionary which associates multiplicity values to the k-mers in s
    """
    WMD = dict()
    for i in range(len(s) -k +1):
        w = s[i:i+k]
        WMD[w] = WMD.get(w,0) + 1
    return WMD
        
    
def fast_k_entropy(s,k):
    """

        Calculate the empirical k-entropy on k-mers in s
    -------
    Parameters:
        s (str) : the input string
        k (int) : the length of the k-mer
    -------
    Returns:
        -e (float) = k - entropy on k-mers in s
    """
    distr = get_multiplicity_distribution(s,k)
    t = sum(distr.values())
    e = 0.0
    for v in distr.values():
        e += math.log(v / t, 2)
    return -e

def wld(s, k_start, k_end):
    """

        Calculate the word lenght distribution of the string s for the given range of values of word length k
    -------
    Paramters:
        s (str) : the input string
        k_start (int) : the initial word length
        k_end (int) : the final word length
    -------
    Returns:
            dict[int,int] : a dictionary which associates world lengths (key) to the number of k-mers at each length (value)
    """
    wld = dict()
    for k in range(k_start,k_end):
        wld[k] = len(get_kmers(s,k))
        
    plot_wld(wld, k_start, k_end)    
    return wld


def plot_wld(wld, k_start, k_end):
    """

        Plots the word length distrubution 
        -------
        Paramters:
            wld (dict[int,int]) : a dictionary which associates world lengths (key) to the number of k-mers at each length (value)
            k_start (int) : the initial word length
            k_end (int) : the final word length
        -------
        Returns:
            void
    """   
    import matplotlib.pyplot as plt
   
    bar_values = [v for k,v in sorted(wld.items())]
    plt.rcParams['figure.figsize'] = [20, 6]
    plt.bar(range(k_start,k_end), bar_values)
    plt.xticks(range(k_start,k_end), range(k_start,k_end))
    plt.ylabel('|D_k(G)|')
    plt.xlabel('k')
    plt.title('Word length distribution')
    plt.show()
    
    
def amd(s, k_start, k_end):
    """

        Calculate the average multiplcity distribution of the string s for the given range of values of word length k
        -------
        Paramters:
            s (str) : the input string
            k_start (int) : the initial word length
            k_end (int) : the final word length
        -------
        Returns:
            dict[int,int] : a dictionary which associates word lengths (key) to the average multiplicity at the specific word length (value)
    """
    import statistics 
    amd = dict()
    for k in range(k_start,k_end):
        amd[k] = statistics.mean( get_multiplicity_distribution(s,k).values() )
        
    plot_amd(amd, k_start, k_end)
    return amd


def plot_amd(amd, k_start, k_end):
    """

        Plots the average multiplcity distribution 
        -------
        Paramters:
            amd (dict[int,int]) : a dictionary which associates word lengths (key) to the average multiplicity at the specific word length (value)
            k_start (int) : the initial word length
            k_end (int) : the final word length
        -------
        Returns: 
            void
    
    """  
    import matplotlib.pyplot as plt
    
    bar_values = [v for k,v in sorted(amd.items())]
    plt.rcParams['figure.figsize'] = [20, 6]
    plt.bar(range(k_start,k_end), bar_values)
    plt.xticks(range(k_start,k_end), range(k_start,k_end))
    plt.ylabel('Average multiplicity')
    plt.xlabel('k')
    plt.title('Average multiplicity distribution')
    plt.show()
    
    
def eed(s, k_start, k_end):
    """

        Calculate the empirical entropy distribution of the string s for the given range of values of word length k
        -------
        Paramters:
            s (str) : the input string
            k_start (int) : the initial word length
            k_end (int) : the final word length
        -------
        Returns:
            dict[int,int] : a dictionary which associates word lengths (key) to the empirical entropy at the specific word length (value)
    """
    eed = dict()
    for k in range(k_start,k_end):
        eed[k] = fast_k_entropy(s,k)
    return eed


def plot_eed(eed, k_start, k_end):
    """

        Plots the empirical entropy distribution
        -------
        Paramters:
            eed (dict[int,int]) : a dictionary which associates word lengths (key) to the empirical entropy at the specific word length (value)
            k_start (int) : the initial word length
            k_end (int) : the final word length
        -------
        Returns:
            void
    """  
    import matplotlib.pyplot as plt
    
    bar_values = [v for k,v in sorted(eed.items())]
    plt.rcParams['figure.figsize'] = [20, 6]
    plt.bar(range(k_start,k_end), bar_values)
    plt.xticks(range(k_start,k_end), range(k_start,k_end))
    plt.ylabel('k-entropy')
    plt.xlabel('k')
    plt.title('Empirical entropy distribution')
    plt.show()



def wcmd(s,k):
    """

        Calculate the word co-multiplicity distribution of the string s for the given value of word length k
        -------
        Paramters:
            s (str) : the input string
            k (int) : the word length
        -------
        Returns:
            dict[int,int] : a dictionary which associates a multiplicity value (key) to the number of k-mers having such multiplicity (value)
    """
    distr = dict()
    mdistr = get_multiplicity_distribution(s,k)
    for m in mdistr.values():
        distr[m]= distr.get(m,0) + 1
    return distr


def plot_wcmd(wcmd1):    
    """

        Plots the word co-multiplicity distribution
        -------
        Paramters:
            dict[int,int] : a dictionary which associates a multiplicity value (key) to the number of k-mers having such multiplicity (value)  
        -------
        Returns:
            void
    """     
    import matplotlib.pyplot as plt
    bar_values = [v for k,v in sorted(wcmd1.items())]
    plt.rcParams['figure.figsize'] = [20, 6]
    plt.bar(sorted(wcmd1.keys()), bar_values, width=1.0)
    plt.ylabel('Number of words')
    plt.xlabel('Multiplicity')
    plt.title('Word co-multiplicity distribution')
    plt.show()
    

    
def get_suffix_array(s):
    """

        Construct the suffix array of the string s.
    -------
    Parameters:
        s (str) : the input string
    -------
    Returns:
        sa (list()) : the suffix array of s  
    """
    
    pairs = list()
    for i in range(len(s)):
        pairs.append( (s[i:],i) ) 
    sa = list()
    for p in sorted(pairs):
        sa.append(p[1])
    return sa


def print_suffix_array(s, suffixArray):
    """

        This function prints the suffix array of a string s  
    -------
    Parameters:
            s (str) : the input string
            suffixArray (list()) : the suffix array of s
    -------
    Returns:
        void
    """
    for i in range(len(suffixArray)):
        print(s[suffixArray[i]:] + ' '*(suffixArray[i]), suffixArray[i])
        
def longest_prefix_length(s, i, j):
    """

        Calculate the length of the longest common prefix between two suffixes, 
        the one in position i and the other in position j, of a string s
    -------
    Parameters:
        s (str) : the input string
        i (int) : the position of the first suffix
        j (int) : the position of the second suffix
    -------
    Returns:
        l (int) : the length of the longest common prefix between i and j         
    """
    l = 0
    while (i+l < len(s)) and (j+l < len(s)):
        if s[i+l] != s[j+l]:
            break
        l += 1
    return l


def get_lcp(s,sa):
    """

        Construct the LCP array associated tot he suffix array (sa) of the string s.
        The LCP value of the first suffix is set to be 0.
    -------
    Parameters:
        s (str) : the input string
        sa (list()) : the suffix array of s
    -------
    Returns:
        lcp (list()) : the list of the longest common prefix
    
    """
    lcp = list()
    lcp.append(0)
    for i in range(1,len(sa)):
        lcp.append(longest_prefix_length(s, sa[i], sa[i-1]))
    return lcp


def print_sa_lcp(s,sa,lcp):
    """

        This function prints the suffix array and the longest common prefix of a string s
    -------
    Parameters: 
        s (str) : the input string
        sa (list()) : the suffix array of s
        lcp (list()) : the list of longest common prefix
    -------
    Returns: 
        void
    """
    print('index', 'suffixes' + ' '*(len(s)-len('suffixes')), 'SA', 'LCP', sep='\t')
    print('-'*45)
    for i in range(len(sa)):
        print(i, s[sa[i]:] + ' '*(sa[i]), sa[i], lcp[i], sep='\t')
        

def print_sa_lcp_region(s,sa,lcp, i,j):
    """

        This function prints the suffix array and the longest common prefix in a range i-j
    -------
    Parameters: 
        s (str) : the input string
        sa (list()) : the suffix array of s
        lcp (list()) : the list of longest common prefix
        i (int) : the start index
        j (int) : the end index
    -------
    Returns: 
        void
    """ 
    print('-'*40)
    print('interval')
    for x in range(i,j):
        print(x,s[sa[x]:] +' '*(sa[x]), sa[x], lcp[x], sep='\t')
    #print('.'*40)


def distance_to_n(s,i):
    """

        This function returns the distance of the first occurrency of the character 'N' from the index i in the string s
    -------
    Parameters:
        s (str) : the input string
        i (int) : the start index
    -------
    Returns:
        the distance 
    """
    j = i
    while (j<len(s)) and (s[j] != 'N'):
        j += 1
    return j - i

def get_ns_array(s,sa):
    """
        This function calls distance_to_n to count the distance in all the suffixes 
    -------
    Parameters:
        s (str) : the input string
        sa (list()) : the suffix array of s
    -------
    Returns:
        the call to distance_to_n
    """
    return [ distance_to_n(s,sa[i]) for i in range(len(s)) ]

    

def print_sa_lcp_ns(s,sa,lcp, ns):
    """

        This function prints the suffix array, the longest common prefix and nelsa
    -------
    Parameters:
        s (str) : the input string
        sa (list()) : the suffix array of s
        lcp (list()) : the list of the longest common prefix
        ns (list()) : the list of nelsa
    -------
    Returns: 
        void
        
    """
    print('index', 'suffixes' + ' '*(len(s)-len('suffixes')), 'SA', 'LCP', 'NS', sep='\t')
    print('-'*60)
    for i in range(len(sa)):
        print(i, s[sa[i]:] + ' '*(sa[i]), sa[i], lcp[i], ns[i], sep='\t')
        
    

def print_sa_lcp_ns_region(s,sa,lcp,ns, i,j):
    """

        This function prints the suffix array, the longest common prefix and nelsa in a range i-j
    -------
    Parameters:
        s (str) : the input string
        sa (list()) : the suffix array of s
        lcp (list()) : the list of the longest common prefix
        ns (list()) : the list of nelsa
        i (int) : the start index
        j (int) : the end index
    -------
    Returns: 
        void
    """
    print('-'*60)
    print('interval')
    for x in range(i,j):
        print(x,s[sa[x]:] +' '*(sa[x]), sa[x], lcp[x], ns[x], sep='\t')
       
def print_sa_lcp_ns_for_kmers(s, sa, lcp, ns, i, k):
    """

        This function prints the suffix array, the longest common prefix and nelsa based on length of the kmer k
    -------
    Parameters:
        s (str) : the input string
        sa (list()) : the suffix array of s
        lcp (list()) : the list of the longest common prefix
        ns (list()) : the list of nelsa
        i (int) : the start index
        k (int) : the length of kmer
    -------
    Returns: 
        void
    """
    while i < len(s):
        while  (i < len(s)) and  ( (sa[i] > len(s) - k - 1)  or (ns[i] < k) ): # second further condition
            i += 1
        if i == len(s):
            break
            
        j = i+1
        while (j < len(s)) and (lcp[j] >= k) and (ns[i] >= k): # first further condition
            j += 1
                
        print_sa_lcp_ns_region(s,sa,lcp,ns, i,j)
        print('k-mer:', s[ sa[i]:sa[i]+k] )
        i = j
        
def fast_get_ns_array(s, sa): 
    """

        This function prints the suffix array, the longest common prefix and nelsa in a range i-j
    -------
    Parameters:
        s (str) : the input string
        sa (list()) : the suffix array of s
    -------
    Returns: 
        ns (list()) : the list of nelsa
    """
    inv_sa = [0 for _ in range(len(sa))]
    for i in range(len(sa)):
        inv_sa[ sa[i] ] = i
    
    ns = [0 for _ in range(len(sa))]
    lastn = len(s)
    for i in range(len(s)-1,-1,-1):
        if s[i] == 'N':
            lastn = i
        ns[ inv_sa[i] ] = lastn - i
    return ns
                               
    

class my_iterator:
    __i = 0
    __limit = 10
    
    def __init__(self):
        self.__i = 0
        
    def __iter__(self):
        return self
        
    def __next__(self):
        self.__i += 1
        if self.__i <= self.__limit:
            return self.__i
        else:
            raise StopIteration

def m_function():
    raise StopIteration



class ESAIterator:
    __s = None
    __k = 0
    __sa = None
    __lcp = None
    __i = 0
    __j = 0
    
    def __init__(self, s, k, sa = None, lcp = None):
        self.__s = s
        self.__k = k
        
        if sa == None:
            self.build_sa()
        else:
            self.__sa = sa
            
        if lcp == None:
            self.build_lcp()
        else:
            self.__lcp = lcp

    def build_sa(self):
        print("building suffix array...")
        suffixes = list()
        for i in range(len(self.__s)):
            suffixes.append( (self.__s[i:] + self.__s[:i] ,i) ) 
        self.__sa = list()
        for suff in sorted(suffixes):
            self.__sa.append(suff[1])
        print('done')
        
    def longest_prefix_length(s, i, j):
        l = 0
        while (i+l < len(s)) and (j+l < len(s)):
            if s[i+l] != s[j+l]:
                break
            l += 1
        return l

    def build_lcp(self):
        print('building lcp array...')
        self.__lcp = list()
        self.__lcp.append(0)
        for i in range(1,len(self.__sa)):
            self.__lcp.append( ESAIterator.longest_prefix_length(self.__s, self.__sa[i], self.__sa[i-1]) )
        print('done')
    
    def get_sa(self):
        return self.__sa
    
    def get_lcp(self):
        return self.__lcp
        
    def __iter__(self):
        return self
    def __next__(self):
        if self.__i < len(self.__s):
            self.__i = self.__j
            
            while (self.__i < len(self.__s)) and  (self.__sa[self.__i] > len(self.__s) - self.__k - 1):
                self.__i += 1
            if self.__i == len(self.__s):
                raise StopIteration
            self.__j = self.__i+1
            while ( self.__j < len(self.__s) ) and (self.__lcp[self.__j] >= self.__k):
                self.__j += 1
            ret = self.__s[ self.__sa[self.__i] : self.__sa[self.__i] + self.__k ]
            return ret
        else:
            raise StopIteration

    def multiplicity(self):
        return self.__j - self.__i
    
    def positions(self):
        return self.__sa[self.__i : self.__j]
    
    
    
class NESAIterator:
    __s = None
    __k = 0
    __sa = None
    __lcp = None
    __ns = None
    __i = 0
    __j = 0
    
    def __init__(self, s, k, sa = None, lcp = None, ns = None):
        self.__s = s
        self.__k = k
        
        if sa == None:
            self.build_sa()
        else:
            self.__sa = sa
            
        if lcp == None:
            self.build_lcp()
        else:
            self.__lcp = lcp
            
        if ns == None:
            self.build_ns()
        else:
            self.__ns = ns
            

    def get_k(self):
        return self.__k

    def reset(self):  
        self.__i = 0
        self.__j = 0
            
    def build_sa(self):
        print("building suffix array...")
        suffixes = list()
        for i in range(len(self.__s)):
            suffixes.append( (self.__s[i:] + self.__s[:i] ,i) ) 
        print(suffixes)
        self.__sa = list()
        for suff in sorted(suffixes):
            self.__sa.append(suff[1])
        print(self.__sa)
        print('done')
        
        
    def longest_prefix_length(s, i, j):
        l = 0
        while (i+l < len(s)) and (j+l < len(s)):
            if s[i+l] != s[j+l]:
                break
            l += 1
        return l

    def build_lcp(self):
        print('building lcp array...')
        self.__lcp = list()
        self.__lcp.append(0)
        for i in range(1,len(self.__sa)):
            self.__lcp.append( NESAIterator.longest_prefix_length(self.__s, self.__sa[i], self.__sa[i-1]) )
        print('done')
    
    def build_ns(self):
        print('building ns array...')
        inv_sa = [0 for _ in range(len( self.__sa))]
        for i in range(len(self.__sa)):
            inv_sa[  self.__sa[i] ] = i

        self.__ns = [0 for _ in range(len( self.__sa))]
        lastn = len(self.__s)
        for i in range(len(self.__s)-1,-1,-1):
            if self.__s[i] == 'N':
                lastn = i
            self.__ns[ inv_sa[i] ] = lastn - i
        print('done')

    def get_sa(self):
        return self.__sa
    
    def get_lcp(self):
        return self.__lcp
    
    def get_ns(self):
        return self.__ns
    def __iter__(self):
        return self
    def __next__(self):
        if self.__i < len(self.__s):
            self.__i = self.__j
            
            while (self.__i < len(self.__s)) and  ( (self.__sa[self.__i] > len(self.__s) - self.__k - 1) or (self.__ns[self.__i] < self.__k) ):
                self.__i += 1
            if self.__i == len(self.__s):
                raise StopIteration
            self.__j = self.__i+1
            while ( self.__j < len(self.__s) ) and (self.__lcp[self.__j] >= self.__k) and (self.__ns[self.__i] >= self.__k) :
                self.__j += 1
            ret = self.__s[ self.__sa[self.__i] : self.__sa[self.__i] + self.__k ]
            return ret
        else:
            raise StopIteration
            
    def multiplicity(self):
        return self.__j - self.__i
    
    def positions(self):
        return self.__sa[self.__i : self.__j]
 





def RDD(s,w):
    """

        Extract the recurrence distance ditribution (RDD) of the word w in s.
        Given the starting postions of two occurences of w, p1 and p2, the reucrrence distance is calculated as
        p1 - p2
        such that consecutive occurrences are at distance 1.
        -------
        Parameters:
            s (str) : the reference string
            w (str) : the searched substring
        -------
        Returns:
            dict[int,int] : a dictionary mapping recurrence distances to the number of times they occur
    """
    pos = sorted(get_positions(s,w))
    rdd = dict()
    for i in range(2,len(pos)):
        l = pos[i] - pos[i-1] 
        rdd[l] = rdd.get(l,0) + 1
    return rdd


def plot_RDD(rdd, title):
    """

        Plot an RDD distribution adding missing recurring distances, 
        between 1 and the original maximum distance,
        by adding a value of zero in correspondence of them.
        -------
        Parameters: 
            rdd (dict[int,int]) : a dictionary mapping recurrence distances to the number of times they occur
            title (string) : title for the chart
        -------
        Returns:
            void 
    """
    # se a value equal to zero for the missing recurrence distances
    for d in range(0,max(rdd.keys())):
        rdd[d] = rdd.get(d,0) + 0
        
    # module can be imported by uring aliases to refer them
    import matplotlib.pyplot as plt 
    
    # set the figure size
    plt.rcParams['figure.figsize'] = [20, 6]
    # assign height of bars
    bar_values = [v for k,v in sorted(rdd.items())]
    # plot with specific values on the x-axis that are associated to the height
    plt.bar(sorted(rdd.keys()), bar_values, width=1.0)
    # set the label on the y-axis
    plt.ylabel('Number of pairs') 
    # set the label on the x-axis
    plt.xlabel('Recurrence distance')
    # set a title for the chart
    plt.title(title)
    # plot the chart
    plt.show()
    

def aRDD(s,k):
    """

        Computer the average recurrence distance distribution of the complete set of k-mers occuring in s.
        -------
        Parameters:
            s (str) : the string from which extract the RDDs
            k (int) : the word length of the k-mers for which extract the RDD
        -------
        Returns:
            dict[int,float] : a dictionary mapping recurrence distances to the average number of times they occur
    """
    ardd = dict()
    kmers = get_kmers(s,k)
    for kmer in kmers:
        rdd = RDD(s,kmer)
        for distance,value in rdd.items():
            ardd[distance] = ardd.get(distance,0) + value
    for d,v in ardd.items():
        ardd[d] = ardd[d] / len(kmers)
    return ardd

def read_GFF3(FNA_file, GFF3_file):
    """

        This code reads the GFF3 annotation file of the genome in order to extracts
        the parts of it that are covered by gene annotations. Since genes may reside on both strands and they
        also may overlap, thus the sequence coverage is intended as the number of position in the
        5'-3' strand that are covered by at least one gene independently of the strand. 
        We also recall that GFF3 file usually only report annotation coordinates, thus the actual sequence
        must be retrieved from a corresponding FASTA file.
        -------
        Parameters:
            FNA_file (file.fna) 
            GFF3_file (file.gff3) 
        -------
        Returns: 
            ncseq (str) : 
            cseq (str) : 
    """    
    genome = ''
    for line in open(FNA_file, 'r'):
        if line.strip()[0] != '>':
            genome += line.strip()
    coverage = [0 for i in range(len(genome))]
    
    for line in open(GFF3_file, 'r'):
        if line[0] != "#":
            cc = line.split('\t')
            if len(cc) >= 6:
                if (cc[2] == 'gene'):# and (cc[6] == '+'): # we calculate the coverage of both strands as a single strand
                    start = int(cc[3])
                    end = int(cc[4])
                    for i in range(start, end):
                        coverage[i] += 1

    print('sequence coverage',   (len(coverage) - coverage.count(0)) / len(coverage))

    # sequence of non-coding portion of the genome
    ncseq = ''.join([ genome[i] for i in range(len(genome)) if coverage[i] == 0 ])
    
    # sequence of coding portion of the genome
    cseq = ''.join([ genome[i] for i in range(len(genome)) if coverage[i] > 0 ])
    
    print('total length', len(genome),', non-coding length',len(ncseq), ', protein-coding length', len(cseq))
    
    return ncseq, cseq

    

def lex_order_code(kmer, alphabet):
    """

        This function returns the code in the lexicographical order corresponding to the input kmer.
        -------
        Parameters:
            kmer (str) : the kmer
            alphabet (dict()) : the dictionary -key/value- of the alphabet. 
        -------
        Returns:
            code (int) : the code in the lexicographical order
    """
    code = 0
    l = len(kmer)-1
    k = len(alphabet)
    keys = alphabet.keys()
    for i in range(len(kmer)-1, -1, -1):
        if(kmer[i] not in keys):
            print("Character "+kmer[i]+" at position "+str(i+1)+" is not present in the alphabet.")
            return -1  
        code += alphabet[kmer[i]]*(k**(l-i))
    return code



class NESAnumpy: 
    
    __s = None
    __k = 0
    __sa = None
    __lcp = None
    __ns = None
    __i = 0
    __j = 0
    
    def __init__(self, s, k, sa = None, lcp = None, ns = None):
        self.__s = s
        self.__k = k
        
        if sa == None:
            self.build_sa()
        else:
            self.__sa = sa
            
        if lcp == None:
            self.build_lcp()
        else:
            self.__lcp = lcp
            
        if ns == None:
            self.build_ns()
        else:
            self.__ns = ns


    def get_k(self):
        return self.__k

    def reset(self):  
        self.__i = 0
        self.__j = 0
      
    def build_sa(self):
        print("building suffix array...")
        l = len(self.__s)
        suffixes = np.chararray(l, l) 
        for i in range(l):
            suffixes[i] = (self.__s[i:] + self.__s[:i]) 
        #print(suffixes)
        if l<=(2**8):
            self.__sa = np.zeros(l, np.uint8)
        elif l<=(2**16):
            self.__sa = np.zeros(l, np.uint16)
        elif l<=(2**32):
            self.__sa = np.zeros(l, np.uint32)
        else:
            self.__sa = np.zeros(l, np.uint)
        for i, idx in enumerate(suffixes.argsort()):
            self.__sa[i] = idx
     
        print(self.__sa)
        print('done')
        
        
    def longest_prefix_length(s, i, j):
        l = 0
        while (i+l < len(s)) and (j+l < len(s)):
            if s[i+l] != s[j+l]:
                break
            l += 1
        return l

    def build_lcp(self):
        print('building lcp array...')
        l = len(self.__s)
        if l<=(2**8):
            self.__lcp = np.zeros(l, np.uint8)
        elif l<=(2**16):
            self.__lcp = np.zeros(l, np.uint16)
        elif l<=(2**32):
            self.__lcp = np.zeros(l, np.uint32)
        else:
            self.__lcp = np.zeros(l, np.uint)
        self.__lcp[0] = (0)
        for i in range(1,l):
            self.__lcp[i] = ( NESAnumpy.longest_prefix_length(self.__s, self.__sa[i], self.__sa[i-1]) )
        print('done')
    
    def build_ns(self):
        print('building ns array...')
        l = len(self.__sa)
        inv_sa = np.zeros(l, np.int)
        for i in range(l):
            inv_sa[  self.__sa[i] ] = i
        if l<=(2**8):
            self.__ns = np.zeros(l, np.uint8)
        elif l<=(2**16):
            self.__ns = np.zeros(l, np.uint16)
        elif l<=(2**32):     
            self.__ns = np.zeros(l, np.uint32)
        else:
            self.__ns = np.zeros(l, np.uint)
        lastn = len(self.__s)
        for i in range(len(self.__s)-1,-1,-1):
            if self.__s[i] == 'N':
                lastn = i
            self.__ns[ inv_sa[i] ] = lastn - i
        print('done')

    def get_sa(self):
        return self.__sa
    
    def get_lcp(self):
        return self.__lcp
    
    def get_ns(self):
        return self.__ns
    def __iter__(self):
        return self
    def __next__(self):
        if self.__i < len(self.__s):
            self.__i = self.__j
            
            while (self.__i < len(self.__s)) and  ( (self.__sa[self.__i] > len(self.__s) - self.__k - 1) or (self.__ns[self.__i] < self.__k) ):
                self.__i += 1
            if self.__i == len(self.__s):
                raise StopIteration
            self.__j = self.__i+1
            while ( self.__j < len(self.__s) ) and (self.__lcp[self.__j] >= self.__k) and (self.__ns[self.__i] >= self.__k) :
                self.__j += 1
            ret = self.__s[ self.__sa[self.__i] : self.__sa[self.__i] + self.__k ]
            return ret
        else:
            raise StopIteration
            
    def multiplicity(self):
        return self.__j - self.__i
    
    def positions(self):
        return self.__sa[self.__i : self.__j]



class NESAOptimized:
    
    __s = None
    __k = 0
    __sa = None
    __lcp = None
    __ns = None
    __i = 0
    __j = 0
    
    def __init__(self, s, k, sa = None, lcp = None, ns = None):
        self.__s = s
        self.__k = k
        
        if sa == None:
            self.build_sa()
        else:
            self.__sa = sa
            
        if lcp == None:
            self.build_lcp()
        else:
            self.__lcp = lcp
            
        if ns == None:
            self.build_ns()
        else:
            self.__ns = ns
            
        print("Memoria occupata suffix array: ", sys.getsizeof(self.__sa))
        print("Memoria occupata longest common prefix: ", sys.getsizeof(self.__lcp))
        print("Memoria occupata nelsa: ",sys.getsizeof(self.__ns))

    def get_k(self):
        return self.__k

    def reset(self):  
        self.__i = 0
        self.__j = 0
            
    def build_sa(self):
        print("building suffix array...")
        suffixes = list()
        for i in range(len(self.__s)):
            suffixes.append( (self.__s[i:] + self.__s[:i] ,i) ) 
        #print(suffixes)
        self.__sa = list()
        for suff in sorted(suffixes):
            self.__sa.append(suff[1])
        print(self.__sa)
        print('done')
        
    
    def longest_prefix_length1(string, start, length, sa):

        rank = list(length)
        for i in range(length):
            rank[sa[i]] = i;
        h = 0;
        lcp = list(length);
        for i in range(length):
            k = rank[i];
            if (k == 0):
                lcp[k] = -1;  
            else:
                j = sa[k - 1];
                while (i + h < length and j + h < length and string[start + i + h] == string[start + j + h]):
                    h = h+1;
                lcp[k] = h
        if (h > 0):
            h=h-1;         
        return lcp;

    
    def build_lcp(self):
        print('building lcp array...')
        self.__lcp = NESAOptimized.longest_prefix_length1(self.__s, 0, self.__s.length, self.__sa)
        print('done')


    def build_ns(self):
        print('building ns array...')
        inv_sa = [0 for _ in range(len( self.__sa))]
        for i in range(len(self.__sa)):
            inv_sa[  self.__sa[i] ] = i

        self.__ns = [0 for _ in range(len( self.__sa))]
        lastn = len(self.__s)
        for i in range(len(self.__s)-1,-1,-1):
            if self.__s[i] == 'N':
                lastn = i
            self.__ns[ inv_sa[i] ] = lastn - i
        print('done')

    def get_sa(self):
        return self.__sa
    
    def get_lcp(self):
        return self.__lcp
    
    def get_ns(self):
        return self.__ns
    def __iter__(self):
        return self
    def __next__(self):
        if self.__i < len(self.__s):
            self.__i = self.__j
            
            while (self.__i < len(self.__s)) and  ( (self.__sa[self.__i] > len(self.__s) - self.__k - 1) or (self.__ns[self.__i] < self.__k) ):
                self.__i += 1
            if self.__i == len(self.__s):
                raise StopIteration
            self.__j = self.__i+1
            while ( self.__j < len(self.__s) ) and (self.__lcp[self.__j] >= self.__k) and (self.__ns[self.__i] >= self.__k) :
                self.__j += 1
            ret = self.__s[ self.__sa[self.__i] : self.__sa[self.__i] + self.__k ]
            return ret
        else:
            raise StopIteration
            
    def multiplicity(self):
        return self.__j - self.__i
    
    def positions(self):
        return self.__sa[self.__i : self.__j]






    





        
