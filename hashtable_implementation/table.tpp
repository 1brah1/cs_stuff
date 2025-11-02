/* TODO: Implement the functions for the class Table and Table::Filter */
template <typename T>
void Table::addPrimitiveColumn(string name, const T& default_value)
{
    if(default_fields.get(name)!=nullptr)
    {
        return;
    }
    PrimitiveField<T>* new_f=new PrimitiveField<T> (name,default_value);
    default_fields.insert(name, new_f);
    BST<T, HashTable<Entry*>>* tree= new BST<T, HashTable<Entry*>>();
    index_trees.insert(name,static_cast<BaseBST*>(tree));
    vector<Entry*> current_entries= entries.to_vector();
    for (int i=0;i<entries.size();i++)
    {
        new_f->handleAddEntryToIndexTree(tree,current_entries[i]);
        
    }
}

template <typename T>
void Table::addListColumn(string name, const vector<T>& default_value)
{
    if(default_fields.get(name)!=nullptr)
    {
        return;
    }
    ListField<T>* new_f=new ListField<T> (name,default_value);
    default_fields.insert(name, new_f);
    BST<T, HashTable<Entry*>>* tree= new BST<T, HashTable<Entry*>>();
    index_trees.insert(name,static_cast<BaseBST*>(tree));
    vector<Entry*> current_entries= entries.to_vector();
    for (int i=0;i<entries.size();i++)
    {
        new_f->handleAddEntryToIndexTree(tree,current_entries[i]);
        
    }

}


void Table::addEntry(const Entry& entry) 
{
    Entry* new_entry = new Entry(entry);
    entries.insert(new_entry);

    BST<string, BaseField*> entry_fields = new_entry->getFields();

    std::vector<BaseField*> default_fields_vec = default_fields.getInorder();
    for (int i = 0; i < default_fields_vec.size(); i++) 
    {
        BaseField* default_field = default_fields_vec[i];
        string field_name = default_field->getName();
        
        // Access the field from the locally stored BST
        BaseField** entry_field_ptr = entry_fields.get(field_name);
        BaseBST** index_tree_ptr = index_trees.get(field_name);
        
        if (!index_tree_ptr) continue;
        BaseBST* index_tree = *index_tree_ptr;
        
        if (entry_field_ptr) 
        {
            (*entry_field_ptr)->handleAddEntryToIndexTree(index_tree, new_entry);
        } 
        else 
        {
            default_field->handleAddEntryToIndexTree(index_tree, new_entry);
        }
    }
}





Table::Table(const Table& other) 
{
    
    vector<BaseField*> other_defaults = other.default_fields.getInorder();
    for (BaseField* field : other_defaults) 
    {
        BaseField* cloned = field->clone();
        default_fields.insert(cloned->getName(), cloned);
    }

    for (BaseField* field : other_defaults) 
    {
        string col = field->getName();
        // Use the same type as addPrimitiveColumn/addListColumn
        BST<string, HashTable<Entry*>>* new_tree = new BST<string, HashTable<Entry*>>();
        index_trees.insert(col, static_cast<BaseBST*>(new_tree));
    }

    vector<Entry*> other_entries = other.entries.to_vector();
    for (Entry* og_entry : other_entries) 
    {
        Entry* new_entry = new Entry(*og_entry);
        entries.insert(new_entry);

        
        for (BaseField* field : other_defaults)
        {
            string col = field->getName();
            BaseBST** tree_ptr = index_trees.get(col);
            if (!tree_ptr) 
            {
                continue;
            }
            BaseField** ptr = new_entry->getFields().get(col);
            BaseField* default_field = *default_fields.get(col);
            default_field->handleAddEntryToIndexTree(*tree_ptr, new_entry);
            
        }
    }
}



Table& Table::operator=(const Table& other) 
{
    if (this != &other) 
    {
        vector<BaseField*> other_defaults = other.default_fields.getInorder();
        for (BaseField* field : other_defaults) 
        {
            BaseField* cloned = field->clone();
            default_fields.insert(cloned->getName(), cloned);
        }

        for (BaseField* field : other_defaults) 
        {
            string col = field->getName();
            BST<string, HashTable<Entry*>>* new_tree = new BST<string, HashTable<Entry*>>();
            index_trees.insert(col, static_cast<BaseBST*>(new_tree));
        }
        vector<Entry*> other_entries = other.entries.to_vector();
        for (Entry* og_entry : other_entries) 
        {
            Entry* new_entry = new Entry(*og_entry);
            entries.insert(new_entry);

        
            for (BaseField* field : other_defaults)
            {
                string col = field->getName();
                BaseBST** tree_ptr = index_trees.get(col);
                if (!tree_ptr) 
                {
                    continue;
                }
                BaseField** ptr = new_entry->getFields().get(col);
                BaseField* default_field = *default_fields.get(col);
                default_field->handleAddEntryToIndexTree(*tree_ptr, new_entry);
            
            }
        }
    }
    return *this;
}


Table::~Table() {
    vector<Entry*> entries_vectors = entries.to_vector();
    for (Entry* entry : entries_vectors) 
    {
        delete entry;
    }
    vector<BaseField*> defaults_vectors = default_fields.getInorder();
    for (BaseField* field : defaults_vectors) 
    {
        delete field;
    }
    vector<BaseBST*> index_vectors = index_trees.getInorder();
    for (BaseBST* tree : index_vectors) 
    {
        delete tree;
    }
}

template <typename T>
Table Table::Filter<T>::operator==(const T& value) const {
    Table result;
    vector<BaseField*> og_defaults = table->default_fields.getInorder();
    for (BaseField* field : og_defaults) 
    {
        BaseField* cloned = field->clone();
        result.default_fields.insert(cloned->getName(), cloned);
    }
    BaseBST** tree_ptr = table->index_trees.get(field_name);
    if (!tree_ptr) 
    {
        return result;
    }
    BaseBST* tree = *tree_ptr;
    BST<T, HashTable<Entry*>>* casted_tree = dynamic_cast<BST<T, HashTable<Entry*>>*>(tree);
    if (casted_tree) 
    {
        HashTable<Entry*>* entries_hashtable = casted_tree->get(value);
        if (entries_hashtable!=nullptr) 
        {
            vector<Entry*> vector_entry = entries_hashtable->to_vector();
            for (Entry* entry : vector_entry) 
            {
                result.addEntry(*entry);
            }
        }
    }

    return result;
}


/* Write your code below */