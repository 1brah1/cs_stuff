/* TODO: Implement the functions for the class HashTable */
template <typename T>
HashTable<T>::HashTable(int base_exponent, double max_load_factor)
{
    head_node= new TableNode;
    head_node->table_size=0;
    head_node->exponent_size=base_exponent;
    total_size=0;
    head_node->next=nullptr;
    head_node->table=new vector<T>[1<<base_exponent];
    cur_node=head_node;
    this->max_load_factor=max_load_factor;


}
template <typename T>
HashTable<T>::~HashTable()
{
    TableNode* current=head_node;
    while(current!=nullptr)
    {
        TableNode* next=current->next;
        delete[] current->table;
        delete current;
        current=next;

    }
}
template <typename T>
HashTable<T>::HashTable(const HashTable<T>& other)
{
    total_size=other.total_size;
    max_load_factor=other.max_load_factor;
    if(other.head_node==nullptr)
    {
        head_node=nullptr;
        cur_node=nullptr;
        return;
    }
    head_node= new TableNode{other.head_node->table_size,other.head_node->exponent_size,new vector<T>[1<<other.head_node->exponent_size],nullptr};
    copy(other.head_node->table,other.head_node->table+(1 << other.head_node->exponent_size),head_node->table);
    TableNode* oc=other.head_node->next;
    TableNode* previous=head_node;
    while(oc!=nullptr)
    {
        TableNode* new_Node = new TableNode{oc->table_size,oc->exponent_size,new vector<T>[1<<oc->exponent_size],nullptr};
        copy(oc->table,oc->table+(1 << oc->exponent_size),new_Node->table);
        previous->next = new_Node;
        previous = new_Node;
        oc = oc->next;
    }
    cur_node=previous;
}
template <typename T>
HashTable<T>& HashTable<T>::operator=(const HashTable<T>& other)
{
    if (this!=&other)
    {
        this->~HashTable();
        new (this)HashTable(other);
    }

}
template <typename T>
bool HashTable<T>::exists(const T& value) const
{
    TableNode* cur=head_node;
    while(cur!=nullptr)
    {
        int num_buckets=1<<cur->exponent_size;
        unsigned int hash_value=pa3_hash(value);
        int index=hash_value%num_buckets;
        vector<T>&bucket=cur->table[index];
        typename vector<T>:: iterator it=bucket.begin();
        while(it!=bucket.end())
        {
            if (*it==value)
            {
                return true;
            }
            it++;
        }
        cur=cur->next;

    }
    return false;
}

template <typename T>
bool HashTable<T>::insert(const T& value)
{
    if(exists(value))
    {
        return false;
    }
    int num_buckets=1<<cur_node->exponent_size;
    if ((cur_node->table_size+1)/static_cast<double>(num_buckets)>=max_load_factor)
    {
        TableNode* new_node= new TableNode;
        new_node->exponent_size=cur_node->exponent_size+1;
        new_node->table_size=0;
        new_node->table= new vector<T>[1<<new_node->exponent_size];
        new_node->next=nullptr;
        cur_node->next=new_node;
        cur_node=new_node;

    }
    unsigned int hash_value=pa3_hash(value);
    int index=hash_value%(1<<cur_node->exponent_size);
    cur_node->table[index].push_back(value);
    total_size++;
    cur_node->table_size++;
    return true;
}
template <typename T>
bool HashTable<T>::remove(const T& value)
{
    TableNode* previous=nullptr;
    TableNode* current=head_node;
    while(current)
    {
        int num_buckets=1<<current->exponent_size;
        unsigned int hash_value=pa3_hash(value);
        int index=hash_value%num_buckets;
        vector<T> &bucket=current->table[index];
        typename std::vector<T>::iterator it = bucket.begin();
        while (it != bucket.end()) 
        {
            if (*it == value) 
            {
                break;
            }
            ++it;
        }
        if (it!=bucket.end())
        {
            bucket.erase(it);
            current->table_size--;
            total_size--;
            if (current->table_size==0 && current!=head_node)
            {
                if (previous!=nullptr)
                {
                    previous->next=current->next;

                }
                if (current==cur_node)
                {
                    cur_node=previous;
                }
                delete[] current->table;
                delete current;
            }
            return true;
        }
        previous=current;
        current=current->next;


    }
    return false;

}
template <typename T>
std::vector<T> HashTable<T>::to_vector() const {
    vector<T> result;
    TableNode* current = head_node;
    while (current != nullptr) {
        int num_buckets= 1<<current->exponent_size;
        for (int i = 0; i< num_buckets; i++) 
        {
            typename std::vector<T>::iterator it;
            for (it=current->table[i].begin(); it!= current->table[i].end(); ++it) 
            {
                result.push_back(*it);
            }
        }
        current = current->next;
    }
    return result;
}

/* Write your code below */